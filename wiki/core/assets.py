import json
from pathlib import Path
from urllib.parse import urljoin

from flask import Flask, g


class AssetManager:
    def __init__(self, entry="wiki/core/assets/js/main.js"):
        self._vite_entry = entry
        self._vite_dev_server = "http://localhost:5173"

        self._global_styles = []
        self._global_script_links = []
        self._global_scripts = []

        self._manifest = None

    def init_app(self, app: Flask):

        app.add_template_global(self.render_style_tags, "style_tags")
        app.add_template_global(self.render_script_tags, "script_tags")

        @app.before_request
        def _init_request_assets():
            g.asset_styles = []
            g.asset_script_links = []
            g.asset_scripts = []

        if app.debug:
            self._init_vite_dev()
        else:
            self._init_vite_manifest(app)

    def _init_vite_dev(self):

        client = urljoin(self._vite_dev_server, "@vite/client")
        entry = urljoin(self._vite_dev_server, self._vite_entry)

        self._global_script_links.append(
            f"<script type='module' src='{client}'></script>"
        )

        self._global_script_links.append(
            f"<script type='module' src='{entry}'></script>"
        )

    def _init_vite_manifest(self, app):

        manifest_path = Path(app.root_path) / "static/dist/manifest.json"

        if not manifest_path.exists():
            return

        with open(manifest_path) as f:
            self._manifest = json.load(f)

        entry = self._manifest.get(self._vite_entry)

        if not entry:
            return

        for css in entry.get("css", []):
            self._global_styles.append(
                f"<link rel='stylesheet' href='/static/dist/{css}'>"
            )

        self._global_script_links.append(
            f"<script type='module' src='/static/dist/{entry['file']}'></script>"
        )

    def render_style_tags(self):

        styles = self._global_styles + getattr(g, "asset_styles", [])
        return "\n".join(styles)

    def render_script_tags(self, body=False):

        if body:
            scripts = self._global_scripts + getattr(g, "asset_scripts", [])
        else:
            scripts = self._global_script_links + getattr(g, "asset_script_links", [])

        return "\n".join(scripts)

    def add_style(self, path=None, raw=None):
        if path:
            g.asset_styles.append(f"<link rel='stylesheet' href='{path}'>")
            return

        if raw:
            g.asset_styles.append(f"<style>{raw}</style>")

    def add_script(self, path=None, raw=None, deferred=False):
        if path:
            defer = " defer" if deferred else ""
            g.asset_script_links.append(f"<script src='{path}'{defer}></script>")
            return

        if raw:
            g.asset_scripts.append(f"<script>{raw}</script>")


asset_manager = AssetManager()
