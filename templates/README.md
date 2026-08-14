# Template placeholder tokens

Every `.ldr` file under this directory is an LDraw part list. Each part line looks like:

```
1 <color> x y z ... <part>.dat
```

`combine_modules()` (see `src/services/persona.py`) builds the final model by substituting three dynamic
placeholder tokens wherever they appear as the `<color>` field on a line, before the rest of the pipeline
ever sees the file. All other tokens (e.g. `15`, `70`, `72`) are literal, hardcoded LDraw color codes and
are never touched by substitution.

| Token       | Substituted with                              | Scope                                   |
|-------------|------------------------------------------------|------------------------------------------|
| `0`         | The module's own primary color (`Module.color`) | Per-module, always applied                |
| `SKIN`      | `Persona.skin_tone`                             | Global — applied once across the whole combined document |
| `SECONDARY` | The module's secondary color (`Module.secondary_color`), or the module's primary color if no secondary was supplied | Per-module, always applied |

`SECONDARY` is optional from a template author's perspective: a template file with no `SECONDARY` tokens
works exactly as before (the substitution is a no-op if the token isn't present). But if a template *does*
contain `SECONDARY` tokens and the caller didn't supply `secondary_color` (e.g. the AI pipeline failed to
detect a second color, or a client simply omits it), those parts fall back to the module's primary color
rather than being left un-substituted — this is a deliberate safety net so a missing/bad secondary color
can never produce broken LDraw output, it just quietly renders as a single-color part instead.

**Which parts within a module get marked `SECONDARY` (vs. `0`, `SKIN`, or a fixed literal color) is a
template-authoring decision**, made by hand in an LDraw CAD tool when the `.ldr` file is created — for
example, some `shirt` templates may stay single-color (only ever use `0`), while others may mark sleeves,
trim, or a stripe with `SECONDARY` to render a two-tone shirt; `pants` templates mark shoe parts with
`SECONDARY` so shoes can render a different color from the legs. Application code has no opinion on this
and does not need to know in advance which kind of template was picked, or which module key it belongs to
— it simply substitutes whatever tokens are present, for any module.
