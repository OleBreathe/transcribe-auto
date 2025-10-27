# Auto Transcribe (Whisper + GitHub Actions)

**Как работает:**

1) Кладите аудио в `audio/` и делайте `git push`.
2) Job **Auto Transcribe** (Actions) автоматически:
   - ставит FFmpeg и Python-зависимости,
   - расшифровывает все файлы из `audio/` с помощью Whisper,
   - складывает `.txt`, `.srt`, `.vtt` в `transcripts/<имя_файла>/`,
   - коммитит результат обратно в репозиторий.
3) По умолчанию модель `medium` и язык `ru`. Можно поменять в `.github/workflows/transcribe.yml`.

**Поддерживаемые форматы:** `.ogg`, `.mp3`, `.wav`, `.m4a`, `.mp4`, `.aac`, `.flac`.

---

## Локальный запуск (по желанию)

```bash
pip install -r requirements.txt
python scripts/transcribe.py --model medium --lang ru --in audio --out transcripts
```

Полученные файлы появятся в `transcripts/`.
