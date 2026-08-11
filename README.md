# Alexander Chen — Engineering Portfolio

A static portfolio site rebuilt from the Google Sites version + the "Alex Chen Portfolio" slide deck. Plain HTML/CSS/JS — no build step, no framework, no dependencies to install. Ready to push straight to GitHub Pages.

## What's here

```
index.html          Home — bio, skills, project grid
moonshine.html       Project — Moonshine Engine Chamber
vesper.html          Project — Vesper LOX/IPA Rocket
testing.html         Project — Static Fire Testing
riptide.html         Project — Riptide LOX/LNG Lander
lander-jr.html        Project — Lander Jr GNC test stand
boeing.html          Experience — Boeing internship
robot.html            Project — Golden Oreo competition robot
research.html         Research — Cai Group soft materials
misc.html             Writing — Instructables feature
assets/
  css/style.css       All styling (one file, uses CSS variables)
  js/main.js           Mobile nav, scroll-reveal, image lightbox
  img/                 Photos extracted from the slide deck
build.py               Python generator that produced all the .html files
```

`build.py` is optional — the `.html` files it produced are already sitting in this folder and are what actually gets deployed. Keep `build.py` around if you want to edit copy/content later without hand-editing HTML (see **Editing content** below); otherwise you can delete it and just hand-edit the HTML files directly.

## Deploying to GitHub Pages

1. Create a new repo on GitHub (e.g. `alexchen-portfolio`).
2. Push everything in this folder to the repo root:
   ```bash
   cd portfolio-site
   git init
   git add .
   git commit -m "Initial portfolio site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Source → Deploy from a branch → `main` / `(root)`** → Save.
4. Your site will be live at `https://<your-username>.github.io/<repo-name>/` within a minute or two.

If you want it at `https://<your-username>.github.io/` directly (no repo-name path), name the repo exactly `<your-username>.github.io`.

## Editing content

Every page is plain HTML with plain CSS — open any `.html` file and edit the text directly, no build step required.

If you'd rather edit content in one place and regenerate all pages (keeps formatting/structure consistent), edit the Python dictionaries/strings inside `build.py` (each project page is one function call near the bottom, e.g. `build_moonshine()`), then run:
```bash
python3 build.py
```
This overwrites the `.html` files in place.

## Adding photos to the text-only pages

Boeing, Robot, Research, and Misc currently use a simple line-icon instead of a photo, since no cleared/extracted photography was available for those sections. To add real photos later:

1. Drop the image into `assets/img/`.
2. In `build.py`, find the relevant `project_page(...)` call (e.g. `build_boeing()`) and change `hero_icon="factory"` to `hero_img="assets/img/your-photo.jpg"`.
3. Re-run `python3 build.py`.

## A couple of things worth knowing

- **Phone number in the footer**: the footer includes the email and phone number from the original site. That's now permanently in a public GitHub repo's history if you push it — remove it from `build.py` (`PHONE = ...`) if you'd rather not have that indexed/scraped.
- **Fonts** load from Google Fonts via `@import` in `style.css` (Space Grotesk, IBM Plex Sans, IBM Plex Mono) — this needs internet access to render correctly, which is a non-issue once hosted, but system fonts will show briefly/permanently if someone views it offline.
- All images were extracted and re-compressed from your slide deck PDF, so they're already reasonably sized for the web (15–320 KB each).
