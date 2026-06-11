#!/usr/bin/env python3
"""Regenerate the <main> section of gallery.html from image files in folders.

Usage:
  python scripts/update_gallery.py --root . --gallery gallery.html

By default it scans the working directory for subfolders, sorts them, and
inserts a <section> per folder containing all images with common extensions.
"""
import os
import re
import argparse
from pathlib import Path

DEFAULT_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')


def title_from_folder(name: str) -> str:
    name = re.sub(r'^\d+_', '', name)
    return name.replace('_', ' ').strip().title()


def sanitize_id(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def natural_key(s: str):
    """Return a key for natural sorting: splits numbers and text so
    '10.jpg' sorts after '2.jpg'."""
    parts = re.split(r'(\d+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def build_main(root: Path, folders, exts):
    lines = ['  <main>', '']
    for folder in folders:
        folder_path = root / folder
        if not folder_path.is_dir():
            continue
        files = [f for f in sorted(os.listdir(folder_path), key=natural_key) if not f.startswith('.') and f.lower().endswith(exts)]
        if not files:
            continue
        title = title_from_folder(folder)
        fid = sanitize_id(folder)
        lines.append(f'    <section class="album" id="{fid}">')
        lines.append(f'      <h2>{title}</h2>')
        lines.append('      <div class="grid">')
        for f in files:
            rel = (Path(folder) / f).as_posix()
            lines.append(f'        <img src="{rel}">')
        lines.append('      </div>')
        lines.append('    </section>')
        lines.append('')
    lines.append('  </main>')
    return '\n'.join(lines)


def replace_main_in_file(gallery_file: Path, main_html: str):
    if not gallery_file.exists():
        # create a minimal scaffold if missing
        scaffold = '<!doctype html>\n<html>\n<head><meta charset="utf-8"><title>Gallery</title></head>\n<body>\n' + main_html + '\n</body>\n</html>\n'
        gallery_file.write_text(scaffold, encoding='utf-8')
        print(f'Created new {gallery_file}')
        return True

    content = gallery_file.read_text(encoding='utf-8')
    new_content, count = re.subn(r'<main>.*?</main>', main_html, content, flags=re.S)
    if count == 0:
        # no existing <main>, insert before </body> if possible
        if '</body>' in content:
            new_content = content.replace('</body>', main_html + '\n</body>')
        else:
            new_content = content + '\n' + main_html
    if new_content == content:
        print('No changes to write.')
        return False
    gallery_file.write_text(new_content, encoding='utf-8')
    return True


def parse_args():
    p = argparse.ArgumentParser(description='Update gallery.html from folders')
    p.add_argument('--root', default='.', help='Root folder to scan (default: .)')
    p.add_argument('--gallery', default='gallery.html', help='Path to gallery HTML file')
    p.add_argument('--exts', nargs='*', default=list(DEFAULT_EXTS), help='Image extensions to include')
    p.add_argument('--dry-run', action='store_true', help='Print generated main HTML but do not write')
    return p.parse_args()


def main():
    args = parse_args()
    root = Path(args.root).resolve()
    gallery_file = Path(args.gallery)
    exts = tuple(e.lower() if e.startswith('.') else '.' + e.lower() for e in args.exts)
    folders = sorted([d for d in os.listdir(root) if (root / d).is_dir()], key=natural_key)
    main_html = build_main(root, folders, exts)

    if args.dry_run:
        print(main_html)
        return

    changed = replace_main_in_file(gallery_file, main_html)
    if changed:
        print(f'Updated {gallery_file}')
    else:
        print('No update necessary')


if __name__ == '__main__':
    main()
