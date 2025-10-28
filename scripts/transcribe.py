import argparse, os, sys, pathlib
import whisper

AUDIO_EXT = {".ogg", ".mp3", ".wav", ".m4a", ".mp4", ".aac", ".flac"}

def iter_audio(root):
    root = pathlib.Path(root)
    for p in root.rglob("*"):
        if p.suffix.lower() in AUDIO_EXT and p.is_file():
            yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="audio", help="Входная папка с аудио")
    ap.add_argument("--out", dest="out", default="transcripts", help="Куда класть транскрипты")
    ap.add_argument("--model", default="medium", help="tiny/base/small/medium/large")
    ap.add_argument("--lang", default="ru", help="Язык речи (например, ru)")
    args = ap.parse_args()

    model = whisper.load_model(args.model)
    in_dir = pathlib.Path(args.inp)
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    any_found = False
    for src in iter_audio(in_dir):
        any_found = True
        rel = src.relative_to(in_dir)
        stem = rel.with_suffix("").as_posix()

        # Папка под конкретный файл
        target_dir = out_dir.joinpath(rel).with_suffix("")
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"[+] Transcribe: {src}")
        result = model.transcribe(str(src), language=args.lang, task="transcribe", verbose=False)

        # TXT
        txt_path = target_dir.joinpath(f"{src.stem}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"].strip() + "\n")

        # SRT / VTT
        def to_srt(segments):
            lines = []
            for i, seg in enumerate(segments, 1):
                def ts(t):
                    h = int(t//3600); m = int((t%3600)//60); s = t%60
                    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")
                lines.append(str(i))
                lines.append(f"{ts(seg['start'])} --> {ts(seg['end'])}")
                lines.append(seg["text"].strip())
                lines.append("")
            return "\n".join(lines)

        srt_path = target_dir.joinpath(f"{src.stem}.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(to_srt(result["segments"]))

        vtt_path = target_dir.joinpath(f"{src.stem}.vtt")
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n" + to_srt(result["segments"]).replace(",", "."))

    if not any_found:
        print(f"[!] В '{in_dir}' аудио не найдено.")
        sys.exit(0)

if __name__ == "__main__":
    main()
