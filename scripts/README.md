# update_gallery.py — Usage & Notes

This script regenerates the `<main>` section of `gallery.html` by scanning subfolders and inserting one `<section>` per folder containing all image files it finds.

## Purpose

- Keep `gallery.html` in sync with the images present in your album folders (e.g. `1_maroon_saree`, `2_orange_lehenga`, ...).
- Useful when you add/remove photos and want the gallery HTML updated automatically.

## Requirements

- Python 3.6+

## Quick examples

From the project root (recommended):

```bash
python3 scripts/update_gallery.py --root . --gallery gallery.html
```

To preview the generated `<main>` without writing the file:

```bash
python3 scripts/update_gallery.py --root . --gallery gallery.html --dry-run
```

## Command-line options

- `--root`: Root folder to scan for subfolders. Defaults to `.`.
- `--gallery`: Path to the HTML file to update. Defaults to `gallery.html`.
- `--exts`: Space-separated list of extensions to include (e.g. `--exts .jpg .png .svg`).
- `--dry-run`: Print the generated `<main>` to stdout instead of writing the file.

## How it works (brief)

1. Lists top-level directories under `--root` and sorts them.
2. For each directory, collects files whose filenames end with one of the allowed extensions.
3. Builds an HTML `<section class="album">` block per folder with a heading (folder name cleaned up) and a `div.grid` containing `<img src="...">` elements for each image file.
4. Replaces the existing `<main>...</main>` block in the `--gallery` file with the generated block. If `<main>` is not present, the script attempts to insert the block before `</body>` or appends it to the end.

## Notes & tips

- Filenames beginning with `.` are ignored.
- The script treats the folder name (after removing leading digits and underscores) as the section title. Example: `1_maroon_saree` -> `Maroon Saree`.
- IDs for sections are generated from the folder name (lowercased, non-alphanumerics -> `-`).
- It's a good idea to keep a backup of `gallery.html` or use `--dry-run` before writing.
- You can customize which extensions are included with `--exts`.

## Troubleshooting

- If images do not appear, verify the relative `src` paths in the generated HTML match your hosting layout. The script writes paths relative to `--root` (e.g. `1_maroon_saree/photo.jpg`).
- If the replacement did not take effect, confirm the HTML has a `<main>` tag or a `</body>` tag for insertion.

## Want enhancements?

I can add: lazy-loading attributes, thumbnail generation, lightbox integration, or sort/filter options—tell me which and I'll implement it.
