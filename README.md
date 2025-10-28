# Auto Transcribe (Whisper + GitHub Actions)

**Как пользоваться**

1. Кладите аудио в папку `audio/` (через Upload files).
2. Перейдите в **Actions → Auto Transcribe** — запустится job.
3. Готовые `.txt/.srt/.vtt` появятся в `transcripts/<имя_файла>/`.

**Что делает workflow**
- Ставит FFmpeg, Torch (CPU) и openai-whisper.
- Режет файлы из `audio/` на куски по 2 минуты без перекодирования (ffmpeg `-segment_time 120 -c copy`).
- Транскрибирует **папку `audio_sliced/`** и коммитит результаты.

**Советы**
- Файлы ≤ 100 MB — обычный push/Upload. Крупнее — включайте Git LFS.
- Можно сменить модель в `.github/workflows/transcribe.yml` (`small/medium/large`).
