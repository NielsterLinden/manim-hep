---
name: hep-contribute
description: Contribute an animation back to the manim-hep gallery. Covers the privacy scrub (no internal results, private paths, host names, personal names or logos), swapping real data for seeded synthetic data, the gallery folder contract and README header, the checks, the PR checklist, and the fork, branch and pull-request commands, pushing only after the user says yes. Use when the user wants to share, upstream, publish or contribute a scene to manim-hep.
---

# Contributing a scene to the manim-hep gallery

Everything in the gallery is public. Before anything leaves the user's machine, go through
the scrub list with them. **Pushing and opening the pull request happen only after the
user says yes.**

## 1. Privacy scrub (every item, with the user)

- [ ] **No unpublished or internal results.** Replace the data with seeded synthetic data
      of the same shape, or with public data that has a DOI (for example CMS Open Data,
      with the `cms-opendata` label).
- [ ] **No private paths or host names.** Check for `/afs/`, `/eos/`, `/project/`,
      `/data/.../users/`, home folders, `C:\Users\...`, and cluster or node names.
      `manim-hep lint` flags the common ones (MH006).
- [ ] **No personal names** except the contributing author's, no usernames, no e-mail
      addresses, no meeting or committee references.
- [ ] **No logos, experiment branding or copied official figures.** No images of unknown
      origin.
- [ ] **Licences.**
  - The contribution is MIT.
  - Nothing copied from CC BY-SA, NC or proprietary sources. For example, recreate chart
    layouts from scratch rather than following a share-alike original.
  - Every physics fact is cited.
- [ ] **Labels.** Experiment labels on synthetic data use a non-official status (CMS
      "Private work", LHCb "Unofficial", ATLAS "Work in Progress"), with a visible
      "Synthetic data" note.

## 2. Shape it as a gallery example

```
gallery/<category>/[<experiment>/]<slug>/
├── scene.py       imports only manim, manim_hep, numpy and the standard library; seeded
├── README.md      YAML header + what it shows, physics notes with sources, how to adapt it
└── storyline.md   optional: the storyline it was built from (Record without keyframes)
```

- The categories are `theory`, `methods`, `experiments/<generic|atlas|cms|lhcb|km3net>`,
  `plots/<general|atlas|cms|lhcb>` and `ml`.
- Start from `gallery/_template/`.
- README header fields: `title`, `category`, `tags`, `authors`, `data` (`synthetic` or
  `none`), `label_status`, `manim_hep` (version), `scenes` (preview scene first),
  `references`.
- **Promotion rule.** Helpers stay in the scene file. A helper moves into `manim_hep` only
  when a second example needs it: then open a separate PR with tests, following the add-only
  API rule.

## 3. Checks (all must pass locally)

```bash
manim-hep lint gallery/<category>/<slug>
python -m pytest tests/test_gallery.py -k <slug>        # contract + render
manim-hep render gallery/<category>/<slug>/scene.py <Scene>   # look at the frames
```

## 4. Fork, branch, pull request

Run these one by one. Wait for the user's yes before the push.

```bash
gh repo fork NielsterLinden/manim-hep --clone      # once
cd manim-hep
git switch -c gallery/<slug>
# copy the example folder in, run the checks above
git add gallery/<category>/<slug>
git commit -m "gallery: add <slug>"
# ASK THE USER, then:
git push -u origin gallery/<slug>
gh pr create --fill --repo NielsterLinden/manim-hep
```

## PR checklist (paste it into the description)

- [ ] It renders in CI (`gallery.yml`)
- [ ] `manim-hep lint` is clean
- [ ] Synthetic data, or public data with a DOI
- [ ] Physics sources are cited
- [ ] No logos, internal results, private paths, host names or personal names
- [ ] Licence-compatible (MIT; nothing share-alike or non-commercial copied)
