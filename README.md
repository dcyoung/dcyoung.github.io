# Personal Blog ![Release](https://github.com/dcyoung/dcyoung.github.io/actions/workflows/release.yml/badge.svg)

This repository hosts the code for my personal [blog](https://dcyoung.github.io).

The website is powered by [Jekyll](https://jekyllrb.com) — a static site generator written in Python — and uses a theme based on [minimal-mistakes](https://mmistakes.github.io/minimal-mistakes).

## Preview the Website

Serve a local preview with Docker Compose (incremental rebuilds enabled; file watching is off due to a Jekyll 3.9/pathutil crash on this image):

```bash
docker compose up -d
```

Visit [http://localhost:4000](http://localhost:4000). Prefer `docker compose stop` / `docker compose start` over `down` so the named gem cache volume stays warm. Restart the container after content edits to rebuild.

## Hosting

This blog is hosted by [GitHub Pages](https://pages.github.com/). Using Github Actions, continuous integration builds the site every time the source is updated.

## License

The source code for generation of the blog is under MIT License. Content is copyrighted.

## Contact

If you have any questions, you can [email](mailto:david@questionablyartificial.com) me.
