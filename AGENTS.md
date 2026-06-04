# AGENTS.md

## Project overview

This repository is a **GitHub profile README** for [Wozgard/Wozgard](https://github.com/Wozgard/Wozgard). It contains static markdown (`README.md`) and local PNG assets in `img/`. There is no application server, build step, or package manager in this repo.

## Cursor Cloud specific instructions

### Services

| Service | Required? | Notes |
|---------|-----------|-------|
| Git | Yes | Clone, commit, and push README changes |
| Local preview server | Optional | For validating markdown rendering and `./img/` asset paths before push |
| GitHub (remote) | Optional for local dev | Primary deployment target — README renders on the GitHub profile after push to `main` |

No databases, Docker containers, or npm/pip dependencies are part of this repository.

### Lint / test / build

There are no lint, test, or build commands configured. Validation is manual:

- Confirm `README.md` markdown renders correctly
- Confirm `./img/*.png` files exist and are valid PNG images
- Confirm external links (Telegram, LinkedIn, VK) and Devicon badge URLs are correct

### Local preview (optional)

To preview the profile README with working local image paths, generate a temporary preview and serve it (do not commit preview artifacts):

```bash
mkdir -p /tmp/profile-preview
ln -sf /workspace/img /tmp/profile-preview/img
python3 -c "
import markdown
html = markdown.markdown(open('/workspace/README.md').read(), extensions=['extra'])
open('/tmp/profile-preview/index.html','w').write(
  f'<!DOCTYPE html><html><head><meta charset=utf-8><title>Preview</title></head><body>{html}</body></html>'
)"
cd /tmp/profile-preview && python3 -m http.server 8080
```

Open http://127.0.0.1:8080/ in a browser. Use `tmux` if the server should stay running in the background.

If `markdown` is not installed: `pip install markdown` (user-local install is sufficient).

### Workflow

1. Edit `README.md` and/or replace images in `img/`
2. Preview locally (optional)
3. Commit and push to `main`
4. Verify rendering on the GitHub profile page
