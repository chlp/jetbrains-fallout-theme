#!/usr/bin/env python3
"""Generates the Wasteland Terminal JetBrains theme (UI theme JSON + editor colour scheme XML).

The palette below is the single source of truth. Run `python3 generate.py` after editing it;
`build.sh` packs the generated files into an installable plugin jar.
"""
import json
from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).resolve().parent / "src" / "themes"

# --- Palette (shared with the Ghostty theme, plus a few in-between shades) ---------------------
BG = "#050b05"          # editor / terminal background (Ghostty background, palette 0)
FG = "#18ff62"          # main text (Ghostty foreground, palette 2)
CURSOR = "#39ff72"
P1 = "#26b34f"          # palette 1
P3 = "#a1d64b"          # palette 3 (strings)
P4 = "#3e9b67"          # palette 4 (comments)
P5 = "#64b879"          # palette 5
P6 = "#60e899"          # palette 6 (numbers, UI text)
P7 = "#b5ffc5"          # palette 7 (keywords)
ACCENT = "#1f8a3f"      # cmux accent colour
MINT = "#8ef0a8"        # types
PUNCT = "#4fc777"       # operators / punctuation
DIM = "#2c6b3f"         # line numbers, unused code
FAINT = "#1d4a2a"       # whitespace markers
CARET_ROW = "#0a170c"
GUIDE = "#12301a"
SEL = "#1a4d27"
SEL_SOFT = "#123d1e"
ERROR = "#ff7a3d"       # errors: amber-orange, the only "hot" colour
WARNING = "#e6c84a"     # warnings: amber-yellow
ERROR_BG = "#3a1a08"
DELETED = "#c27a2c"

# UI ramps: ExperimentalDark (New UI) references these names everywhere, so overriding them
# re-tints the whole IDE. Index 1 = darkest.
GRAY = ["#050b05", "#081208", "#0f2213", "#143019", "#1a3d21", "#204a29", "#2c6b3f",
        "#3e9b67", "#4aa870", "#56c482", "#60e899", "#8ef0a8", "#b5ffc5", "#e0ffe6"]
BLUE = ["#0c2814", "#10351a", "#15461f", "#1a5727", "#1f6a2f", "#1f8a3f", "#26a04a",
        "#30b856", "#45cf6a", "#66e388", "#8ef0a8", "#b5ffc5", "#d4ffdc"]
GREEN = ["#0a1f0e", "#0d2912", "#12381a", "#184a22", "#1f5e2b", "#2a8a45", "#26b34f",
         "#4fe07a", "#7cf29a", "#a0f7b8", "#c2fbd0", "#e0ffe6"]
YELLOW = ["#211c08", "#3a3110", "#574a17", "#74631e", "#917c25", "#ae952c", "#d6b440",
          "#e6c84a", "#efd775", "#f6e6a0", "#fbf3cc"]
ORANGE = ["#261808", "#3d260d", "#5c3a14", "#7a4d1a", "#995f20", "#c27a2c", "#e08c38",
          "#f0a050", "#f5b878", "#facfa0", "#ffe3c8"]
RED = ["#2a1408", "#34180a", "#4a2210", "#632c14", "#803718", "#a8441c", "#d65a28",
       "#ff7a3d", "#ff9a66", "#ffb894", "#ffd2bb", "#ffe8dc"]
PURPLE = ["#0e2a1f", "#123526", "#16402d", "#1c5238", "#226444", "#2a7a52", "#349464",
          "#4aae7a", "#68c592", "#8ad8ab", "#ade8c5", "#cff5de"]
TEAL = PURPLE


def ramp(name, values):
    return {f"{name}{i}": v for i, v in enumerate(values, 1)}


# --- UI theme ----------------------------------------------------------------------------------
def theme_json(crt=False):
    colors = {}
    for name, values in [("Gray", GRAY), ("Blue", BLUE), ("Green", GREEN), ("Yellow", YELLOW),
                         ("Orange", ORANGE), ("Red", RED), ("Purple", PURPLE), ("Teal", TEAL)]:
        colors.update(ramp(name, values))
    colors.update({
        "Gray1.5": "#071007",
        "Fg": P6,
        "FgBright": P7,
        "FgSecondary": P4,
        "FgDisabled": DIM,
        "Bg": BG,
        "Panel": "#081208",
        "Raised": "#0c1a0d",
        "Hover": "#11261580",
        "Border": "#163a1e",
        "Selection": SEL,
        "SelectionInactive": "#10301a",
        "Accent": ACCENT,
        "Link": P3,
    })

    ui = {
        "*": {
            "foreground": "Fg",
            "background": "Panel",
            "infoForeground": "FgSecondary",
            "disabledForeground": "FgDisabled",
            "disabledText": "FgDisabled",
            "inactiveForeground": "FgDisabled",
            "selectionForeground": "FgBright",
            "selectionInactiveForeground": "Fg",
            "selectionBackground": "Selection",
            "lightSelectionBackground": "SelectionInactive",
            "selectionInactiveBackground": "SelectionInactive",
            "hoverBackground": "Hover",
            "borderColor": "Border",
            "separatorColor": "Border",
            "focusColor": "Accent",
            "focusedBorderColor": "Accent",
            "underlineColor": "Accent",
            "acceleratorForeground": "FgSecondary",
            "modifiedItemForeground": "Link",
        },

        # Islands look (2025.3+); ignored by older IDE versions.
        "Islands": 1,
        "Island": {
            "arc": 20, "arc.compact": 16,
            "borderArcLength": 14, "borderArcLength.compact": 10,
            "borderWidth": 6, "borderWidth.compact": 4,
            "borderColor": "Bg",
            "inactiveAlpha": 0.55,
        },

        "MainWindow.background": "Bg",
        "MainWindow.Tab": {"background": "Bg", "selectedBackground": "Panel",
                           "foreground": "Fg", "hoverBackground": "Hover"},
        "MainToolbar": {"background": "Bg", "inactiveBackground": "Bg",
                        "borderColor": "#00000000",
                        "Dropdown.transparentHoverBackground": "Hover",
                        "Icon.hoverBackground": "Hover"},
        "StatusBar": {"background": "Bg", "borderColor": "#00000000",
                      "Widget.foreground": "FgSecondary", "Breadcrumbs.foreground": "FgSecondary",
                      "Widget.hoverBackground": "Hover", "Breadcrumbs.hoverBackground": "Hover"},
        "ToolWindow": {
            "background": "Panel",
            "Header": {"background": "Panel", "inactiveBackground": "Panel", "borderColor": "Border"},
            "HeaderTab": {"hoverBackground": "Hover", "hoverInactiveBackground": "Hover",
                          "selectedBackground": "Selection", "selectedInactiveBackground": "SelectionInactive",
                          "underlineColor": "Accent"},
            "Button": {"selectedBackground": "Selection", "selectedForeground": "FgBright",
                       "hoverBackground": "Hover"},
            "Stripe": {"background": "Bg", "borderColor": "#00000000", "separatorColor": "Border"},
        },
        "Borders": {"color": "Border", "ContrastBorderColor": "Border"},
        "OnePixelDivider.background": "Border",

        "EditorTabs": {
            "background": "Bg",
            "underTabsBorderColor": "Border",
            "underlineColor": "Accent",
            "underlinedTabBackground": "#0f2614",
            "underlinedTabForeground": "FgBright",
            "inactiveUnderlineColor": "Gray7",
            "hoverBackground": "Hover",
            "selectedForeground": "FgBright",
        },
        "Editor": {"background": "Bg", "foreground": FG,
                   "SearchField": {"background": "Raised", "borderColor": "Border"},
                   "ToolTip": {"background": "Raised", "border": "Border", "foreground": "Fg"}},
        "EditorPane.inactiveBackground": "Bg",

        "Tree": {"background": "Panel", "selectionBackground": "Selection",
                 "selectionInactiveBackground": "SelectionInactive",
                 "selectionForeground": "FgBright", "hoverBackground": "Hover"},
        "List": {"background": "Panel", "selectionBackground": "Selection",
                 "selectionInactiveBackground": "SelectionInactive",
                 "selectionForeground": "FgBright", "hoverBackground": "Hover"},
        "Table": {"background": "Panel", "selectionBackground": "Selection",
                  "selectionInactiveBackground": "SelectionInactive",
                  "stripeColor": "#0a160b", "gridColor": "Border"},

        "Popup": {"background": "Raised", "borderColor": "Border",
                  "Header.activeBackground": "Raised", "Header.inactiveBackground": "Raised",
                  "Advertiser.background": "Raised", "Advertiser.foreground": "FgSecondary",
                  "Toolbar.background": "Raised", "separatorColor": "Border"},
        "PopupMenu": {"background": "Raised"},
        "Menu": {"background": "Raised", "selectionBackground": "Selection",
                 "borderColor": "Border"},
        "MenuItem": {"background": "Raised", "selectionBackground": "Selection",
                     "acceleratorForeground": "FgSecondary"},
        "CompletionPopup": {"background": "Raised", "foreground": "Fg",
                            "matchForeground": "FgBright", "selectionBackground": "Selection",
                            "selectionInactiveBackground": "SelectionInactive"},
        "SearchEverywhere": {"Header.background": "Raised", "List.separatorForeground": "FgSecondary",
                             "SearchField.background": "Raised", "Tab.selectedBackground": "Selection"},
        "ToolTip": {"background": "Raised", "foreground": "Fg", "borderColor": "Border",
                    "infoForeground": "FgSecondary"},
        "ParameterInfo": {"background": "Raised", "foreground": "Fg", "borderColor": "Border"},
        "Notification": {"background": "Raised", "foreground": "Fg", "borderColor": "Border",
                         "MoreButton.background": "Panel"},
        "GotItTooltip": {"background": "Gray5", "borderColor": "Accent", "foreground": "FgBright"},
        "Banner": {"infoBackground": "#0f2a16", "infoBorderColor": "Gray6",
                   "successBackground": "#0f2a16", "successBorderColor": "Green6",
                   "warningBackground": "Yellow1", "warningBorderColor": "Yellow4",
                   "errorBackground": "Red1", "errorBorderColor": "Red4"},
        "InlineBanner": {"hoverBackground": "Hover", "pressedBackground": "#1a4d2780"},
        "NotificationsToolwindow.newNotification.background": "Raised",

        "TextField": {"background": "Bg"},
        "TextArea": {"background": "Bg"},
        "FormattedTextField": {"background": "Bg"},
        "PasswordField": {"background": "Bg"},
        "ComboBox": {"background": "Bg", "nonEditableBackground": "Raised",
                     "ArrowButton.background": "Bg", "ArrowButton.nonEditableBackground": "Raised",
                     "selectionBackground": "Selection"},
        "Component": {"borderColor": "Border", "focusColor": "Accent", "focusedBorderColor": "Accent",
                      "errorFocusColor": ERROR, "warningFocusColor": WARNING,
                      "infoForeground": "FgSecondary"},
        "Button": {
            "startBackground": "Raised", "endBackground": "Raised",
            "startBorderColor": "Border", "endBorderColor": "Border",
            "foreground": "Fg",
            "default": {"startBackground": "Accent", "endBackground": "Accent",
                        "startBorderColor": "Accent", "endBorderColor": "Accent",
                        "foreground": "#e0ffe6", "focusColor": "Blue8"},
        },
        "CheckBox": {"background": "Panel"},
        "Link": {"activeForeground": "Link", "hoverForeground": "FgBright",
                 "pressedForeground": "FgBright", "visitedForeground": "Link"},
        "Hyperlink.linkColor": "Link",
        "ProgressBar": {"progressColor": "Accent", "indeterminateStartColor": "Accent",
                        "indeterminateEndColor": "Blue8", "trackColor": "Gray4",
                        "passedColor": "Green7", "failedColor": ERROR},
        "ScrollBar": {
            "thumbColor": "#2c6b3f80", "hoverThumbColor": "#3e9b67b0",
            "thumbBorderColor": "#00000000", "hoverThumbBorderColor": "#00000000",
            "trackColor": "#00000000", "hoverTrackColor": "#0f221340",
            "Transparent": {"thumbColor": "#2c6b3f80", "hoverThumbColor": "#3e9b67b0",
                            "thumbBorderColor": "#00000000", "hoverThumbBorderColor": "#00000000",
                            "trackColor": "#00000000", "hoverTrackColor": "#0f221340"},
            "Mac": {"thumbColor": "#2c6b3f80", "hoverThumbColor": "#3e9b67b0",
                    "Transparent.thumbColor": "#2c6b3f80", "Transparent.hoverThumbColor": "#3e9b67b0"},
        },
        "Counter": {"background": "Accent", "foreground": "#e0ffe6"},
        "Tag.background": "Gray4",
        "Label": {"infoForeground": "FgSecondary", "errorForeground": ERROR},
        "TitlePane": {"background": "Bg", "inactiveBackground": "Bg"},
        "SidePanel.background": "Panel",
        "Plugins": {"background": "Panel", "Tab.selectedBackground": "Selection",
                    "SearchField.background": "Bg"},
        "WelcomeScreen": {"background": "Bg", "Details.background": "Panel",
                          "SidePanel.background": "Bg", "Projects.background": "Bg",
                          "Projects.selectionBackground": "Selection"},
        "VersionControl": {"Log.Commit.currentBranchBackground": "#0f2614",
                           "FileHistory.Commit.selectedBranchBackground": "#0f2614",
                           "Ref.backgroundBase": "Gray6"},
        "DragAndDrop": {"areaBackground": "#1f8a3f4d", "rowBackground": "#1f8a3f26"},
        "MemoryIndicator": {"usedBackground": "#1f8a3f80", "allocatedBackground": "Gray3"},
        "Badge": {"blueSecondaryBackground": "#1a5727cc", "greenSecondaryBackground": "#184a22cc",
                  "purpleSecondaryBackground": "#1c5238cc"},
        "ActionButton": {"hoverBackground": "Hover", "pressedBackground": "#1a4d2780"},
        "RunWidget": {"background": "Accent", "hoverBackground": "#00000019"},
        "FileColor": {"Gray": "#0f2213", "Blue": "#10351a", "Green": "#12381a",
                      "Orange": "#3d260d", "Rose": "#34180a", "Violet": "#123526",
                      "Yellow": "#3a3110"},
    }

    icons = {
        "ColorPalette": {
            # Old UI icon colours
            "Actions.Grey": P5, "Actions.Red": ERROR, "Actions.Yellow": WARNING,
            "Actions.Green": FG, "Actions.Blue": P6, "Actions.GreyInline.Dark": P4,
            "Objects.Grey": P5, "Objects.RedStatus": ERROR, "Objects.Red": ERROR,
            "Objects.Pink": "#f0a050", "Objects.Yellow": WARNING, "Objects.Green": FG,
            "Objects.Blue": P6, "Objects.Purple": MINT, "Objects.BlackText": "#000000",
            "Objects.YellowDark": "#ae952c", "Objects.GreenAndroid": P1,
            # New UI default icon stroke
            "#CED0D6": P6,
            "Checkbox.Background.Default": BG,
            "Checkbox.Border.Default": P4,
            "Checkbox.Background.Selected": ACCENT,
            "Checkbox.Border.Selected": ACCENT,
            "Checkbox.Foreground.Selected": "#e0ffe6",
            "Checkbox.Focus.Wide": "#30b856",
            "Checkbox.Background.Disabled": "#0f2213",
            "Checkbox.Border.Disabled": DIM,
            "Checkbox.Foreground.Disabled": DIM,
        }
    }

    theme = {
        "name": "Wasteland Terminal CRT" if crt else "Wasteland Terminal",
        "dark": True,
        "author": "chlp",
        "parentTheme": "ExperimentalDark",
        "editorScheme": "/themes/WastelandTerminal.xml",
        "colors": colors,
        "ui": ui,
        "icons": icons,
    }
    if crt:
        # CRT scanlines: a tiled PNG painted under the text of editors and tool windows.
        # Users can tune it in Settings | Appearance | Background Image. The IDE turns the
        # Islands layout off when a background image is set, hence a separate theme.
        theme["background"] = SCANLINES_BG
    return theme


# --- CRT scanlines background --------------------------------------------------------------------
SCANLINE_PERIOD = 3          # one lit line every N pixels (logical pixels)
SCANLINE_COLOR = (0x18, 0xff, 0x62)
SCANLINES_FILE = "crt-scanlines.png"
SCANLINES_BG = {
    "image": f"themes/{SCANLINES_FILE}",   # classloader path: no leading slash
    "transparency": 7,       # opacity in percent; higher = stronger lines
    "fill": "tile",
    "anchor": "top_left",
}


def scanlines_png(width=16):
    """A width x SCANLINE_PERIOD RGBA PNG: first row opaque phosphor green, the rest transparent."""
    import struct
    import zlib

    rows = []
    for y in range(SCANLINE_PERIOD):
        alpha = 255 if y == 0 else 0
        rows.append(b"\x00" + bytes(SCANLINE_COLOR + (alpha,)) * width)

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, SCANLINE_PERIOD, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))


# --- Editor colour scheme ----------------------------------------------------------------------
PLAIN, BOLD, ITALIC, BOLD_ITALIC = 0, 1, 2, 3
UNDERSCORE, WAVE, STRIKEOUT, BOXED = 1, 2, 3, 0


def a(fg=None, bg=None, font=None, effect=None, etype=None, stripe=None):
    return {"FOREGROUND": fg, "BACKGROUND": bg, "FONT_TYPE": font,
            "EFFECT_COLOR": effect, "EFFECT_TYPE": etype, "ERROR_STRIPE_COLOR": stripe}


SCHEME_COLORS = {
    "CARET_COLOR": CURSOR,
    "CARET_ROW_COLOR": CARET_ROW,
    "CONSOLE_BACKGROUND_KEY": BG,
    "GUTTER_BACKGROUND": BG,
    "EDITOR_GUTTER_BACKGROUND": BG,
    "LINE_NUMBERS_COLOR": DIM,
    "LINE_NUMBER_ON_CARET_ROW_COLOR": FG,
    "INDENT_GUIDE": GUIDE,
    "SELECTED_INDENT_GUIDE": DIM,
    "VISUAL_INDENT_GUIDE": "#0f2614",
    "MATCHED_BRACES_INDENT_GUIDE_COLOR": P4,
    "RIGHT_MARGIN_COLOR": GUIDE,
    "SELECTION_BACKGROUND": SEL,
    "SELECTION_FOREGROUND": "",
    "WHITESPACES": FAINT,
    "WHITESPACES_MODIFIED_LINES_COLOR": P4,
    "SOFT_WRAP_SIGN_COLOR": FAINT,
    "METHOD_SEPARATORS_COLOR": "#163a1e",
    "TEARLINE_COLOR": "#163a1e",
    "SELECTED_TEARLINE_COLOR": P4,
    "FOLDED_TEXT_BORDER_COLOR": DIM,
    "ADDED_LINES_COLOR": P1,
    "MODIFIED_LINES_COLOR": P3,
    "DELETED_LINES_COLOR": DELETED,
    "IGNORED_ADDED_LINES_BORDER_COLOR": P1,
    "IGNORED_MODIFIED_LINES_BORDER_COLOR": P3,
    "IGNORED_DELETED_LINES_BORDER_COLOR": DELETED,
    "DIFF_SEPARATORS_BACKGROUND": "#0c1a0d",
    "ANNOTATIONS_COLOR": P4,
    "ANNOTATIONS_LAST_COMMIT_COLOR": P7,
    "VCS_ANNOTATIONS_COLOR_1": "#1a4d27",
    "VCS_ANNOTATIONS_COLOR_2": "#153f20",
    "VCS_ANNOTATIONS_COLOR_3": "#11321a",
    "VCS_ANNOTATIONS_COLOR_4": "#0e2614",
    "VCS_ANNOTATIONS_COLOR_5": "#0b1c0f",
    "DOCUMENTATION_COLOR": "#081208",
    "DOC_COMMENT_GUIDE": FAINT,
    "DOC_COMMENT_LINK": P6,
    "LOOKUP_COLOR": "#0c1a0d",
    "NOTIFICATION_BACKGROUND": "#0f2614",
    "PROMOTION_PANE": "#0f2614",
    "ERROR_HINT": ERROR_BG,
    "INFORMATION_HINT": "#0c1a0d",
    "QUESTION_HINT": "#12301a",
    "HINT_BORDER": "#163a1e",
    "RECENT_LOCATIONS_SELECTION": "#12301a",
    "INLINE_REFACTORING_SETTINGS_DEFAULT": "#0c1a0d",
    "INLINE_REFACTORING_SETTINGS_FOCUSED": "#12301a",
    "INLINE_REFACTORING_SETTINGS_HOVERED": "#0f2614",
    "ScrollBar.Mac.thumbColor": "2c6b3f80",
    "ScrollBar.Mac.hoverThumbColor": "3e9b67b0",
    "ScrollBar.Mac.Transparent.thumbColor": "2c6b3f80",
    "ScrollBar.Mac.Transparent.hoverThumbColor": "3e9b67b0",
    # File name colours in the project tree / tabs / commit dialog
    "FILESTATUS_ADDED": "#c4ee70",
    "FILESTATUS_COPIED": "#c4ee70",
    "FILESTATUS_MODIFIED": P7,
    "FILESTATUS_RENAMED": MINT,
    "FILESTATUS_DELETED": DIM,
    "FILESTATUS_MERGED": WARNING,
    "FILESTATUS_UNKNOWN": ERROR,
    "FILESTATUS_NOT_CHANGED_IMMEDIATE": P7,
    "FILESTATUS_NOT_CHANGED_RECURSIVE": P7,
    "FILESTATUS_IDEA_FILESTATUS_IGNORED": "#7a8a3a",
    "FILESTATUS_IDEA_FILESTATUS_DELETED_FROM_FILE_SYSTEM": DIM,
    "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS": ERROR,
    "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_BOTH_CONFLICTS": ERROR,
    "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_PROPERTY_CONFLICTS": ERROR,
    "FILESTATUS_addedOutside": "#c4ee70",
    "FILESTATUS_modifiedOutside": P7,
    "FILESTATUS_changelistConflict": ERROR,
}

# ANSI colours: 0-7 mirror the Ghostty palette, 8-15 are brighter shades of the same greens.
ANSI = {
    "BLACK": "#0f2213", "RED": P1, "GREEN": FG, "YELLOW": P3, "BLUE": P4, "MAGENTA": P5,
    "CYAN": P6, "GRAY": P7,
    "DARKGRAY": DIM, "RED_BRIGHT": "#3fd068", "GREEN_BRIGHT": "#5cff8f",
    "YELLOW_BRIGHT": "#c4ee70", "BLUE_BRIGHT": "#56bd84", "MAGENTA_BRIGHT": "#84d69a",
    "CYAN_BRIGHT": "#8cf5b8", "WHITE": "#e0ffe6",
}

KEYWORD = a(P7, font=BOLD)
STRING = a(P3)
NUMBER = a(P6)
COMMENT = a(P4, font=ITALIC)
TYPE = a(MINT)
FIELD = a(P7)
FUNC_DECL = a(P6, font=BOLD)
FUNC_CALL = a(FG)
PARAM = a(FG, font=ITALIC)
GLOBAL = a(P5, font=ITALIC)
PUNCTUATION = a(PUNCT)
METADATA = a(P3, font=ITALIC)
TAG = a(P6)
ATTR = a(P5)
CONSTANT = a(P6, font=ITALIC)
BUILTIN = a(P7)
PACKAGE = a(P5)

ATTRS = {
    "TEXT": a(FG, BG),

    # --- Language defaults (every language inherits from these) ---
    "DEFAULT_KEYWORD": KEYWORD,
    "DEFAULT_IDENTIFIER": a(FG),
    "DEFAULT_STRING": STRING,
    "DEFAULT_VALID_STRING_ESCAPE": a(P6, font=BOLD),
    "DEFAULT_INVALID_STRING_ESCAPE": a(ERROR, effect=ERROR, etype=WAVE),
    "DEFAULT_NUMBER": NUMBER,
    "DEFAULT_CONSTANT": CONSTANT,
    "DEFAULT_LINE_COMMENT": COMMENT,
    "DEFAULT_BLOCK_COMMENT": COMMENT,
    "DEFAULT_DOC_COMMENT": COMMENT,
    "DEFAULT_DOC_COMMENT_TAG": a(P5, font=BOLD_ITALIC),
    "DEFAULT_DOC_COMMENT_TAG_VALUE": a(P5, font=ITALIC),
    "DEFAULT_DOC_MARKUP": a(P5, "#081208"),
    "DOC_CODE_INLINE": a(P5, "#0c1a0d"),
    "DOC_CODE_BLOCK": a(P5),
    "DOC_TIPS_SHORTCUT": a(P7, "#0f2614"),
    "DEFAULT_OPERATION_SIGN": PUNCTUATION,
    "DEFAULT_BRACES": PUNCTUATION,
    "DEFAULT_BRACKETS": PUNCTUATION,
    "DEFAULT_PARENTHS": PUNCTUATION,
    "DEFAULT_COMMA": PUNCTUATION,
    "DEFAULT_SEMICOLON": PUNCTUATION,
    "DEFAULT_DOT": PUNCTUATION,
    "DEFAULT_FUNCTION_DECLARATION": FUNC_DECL,
    "DEFAULT_FUNCTION_CALL": FUNC_CALL,
    "DEFAULT_INSTANCE_METHOD": FUNC_CALL,
    "DEFAULT_STATIC_METHOD": a(FG, font=ITALIC),
    "DEFAULT_CLASS_NAME": TYPE,
    "DEFAULT_CLASS_REFERENCE": TYPE,
    "DEFAULT_INTERFACE_NAME": a(MINT, font=ITALIC),
    "DEFAULT_INSTANCE_FIELD": FIELD,
    "DEFAULT_STATIC_FIELD": a(P7, font=ITALIC),
    "DEFAULT_LOCAL_VARIABLE": a(FG),
    "DEFAULT_REASSIGNED_LOCAL_VARIABLE": a(FG, effect=DIM, etype=UNDERSCORE),
    "DEFAULT_REASSIGNED_PARAMETER": a(FG, font=ITALIC, effect=DIM, etype=UNDERSCORE),
    "DEFAULT_GLOBAL_VARIABLE": GLOBAL,
    "DEFAULT_PARAMETER": PARAM,
    "DEFAULT_LABEL": a(P3, font=ITALIC),
    "DEFAULT_METADATA": METADATA,
    "DEFAULT_PREDEFINED_SYMBOL": BUILTIN,
    "DEFAULT_TAG": TAG,
    "DEFAULT_ATTRIBUTE": ATTR,
    "DEFAULT_ENTITY": a(P6, font=ITALIC),
    "DEFAULT_TEMPLATE_LANGUAGE_COLOR": a(FG, "#081a0c"),
    "DEFAULT_HIGHLIGHTED_REFERENCE": a(FG, effect=FG, etype=UNDERSCORE),
    "TYPE_PARAMETER_NAME_ATTRIBUTES": a(MINT, font=ITALIC),
    "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": a(P5),
    "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES": a(FG, effect=DIM, etype=UNDERSCORE),

    # --- Code insight ---
    "ERRORS_ATTRIBUTES": a(effect=ERROR, etype=WAVE, stripe=ERROR),
    "WRONG_REFERENCES_ATTRIBUTES": a(ERROR, stripe=ERROR),
    "Unresolved reference access": a(ERROR, stripe=ERROR),
    "RUNTIME_ERROR": a(effect=ERROR, etype=WAVE, stripe=ERROR),
    "BAD_CHARACTER": a(bg=ERROR_BG, effect=ERROR, etype=WAVE),
    "WARNING_ATTRIBUTES": a(effect=WARNING, etype=WAVE, stripe=WARNING),
    "WEAK_WARNING_ATTRIBUTES": a(effect="#7a8a3a", etype=WAVE),
    "INFO_ATTRIBUTES": a(effect=P4, etype=WAVE),
    "GENERIC_SERVER_ERROR_OR_WARNING": a(effect=WARNING, etype=WAVE, stripe=WARNING),
    "DEPRECATED_ATTRIBUTES": a(effect=P4, etype=STRIKEOUT),
    "MARKED_FOR_REMOVAL_ATTRIBUTES": a(effect=ERROR, etype=STRIKEOUT),
    "NOT_USED_ELEMENT_ATTRIBUTES": a(DIM),
    "TYPO": a(effect=P4, etype=WAVE),
    "TEXT_STYLE_ERROR": a(effect=ERROR, etype=WAVE),
    "TEXT_STYLE_WARNING": a(effect=WARNING, etype=WAVE),
    "TEXT_STYLE_SUGGESTION": a(effect=P4, etype=WAVE),
    "GRAMMAR_ERROR": a(effect=WARNING, etype=WAVE),
    "MATCHED_BRACE_ATTRIBUTES": a(P7, SEL, font=BOLD),
    "UNMATCHED_BRACE_ATTRIBUTES": a(bg=ERROR_BG, stripe=ERROR),
    "MATCHED_TAG_NAME": a(bg=SEL),
    "IDENTIFIER_UNDER_CARET_ATTRIBUTES": a(bg=SEL_SOFT, stripe=P1),
    "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": a(bg="#1d4f2a", stripe=P3),
    "SEARCH_RESULT_ATTRIBUTES": a(bg="#2e5a16", stripe=P3),
    "WRITE_SEARCH_RESULT_ATTRIBUTES": a(bg="#3d4a10", stripe=WARNING),
    "TEXT_SEARCH_RESULT_ATTRIBUTES": a(BG, P3, stripe=P3),
    "HYPERLINK_ATTRIBUTES": a(P6, effect=P6, etype=UNDERSCORE),
    "FOLLOWED_HYPERLINK_ATTRIBUTES": a(P5, effect=P5, etype=UNDERSCORE),
    "INACTIVE_HYPERLINK_ATTRIBUTES": a(effect=P4, etype=UNDERSCORE),
    "CTRL_CLICKABLE": a(P6, effect=P6, etype=UNDERSCORE),
    "FOLDED_TEXT_ATTRIBUTES": a(P5, "#0f2614"),
    "LIVE_TEMPLATE_ATTRIBUTES": a(effect=P3, etype=BOXED),
    "LIVE_TEMPLATE_INACTIVE_SEGMENT": a(P4),
    "TEMPLATE_VARIABLE_ATTRIBUTES": a(P3, font=ITALIC),
    "TODO_DEFAULT_ATTRIBUTES": a(P3, font=BOLD_ITALIC, stripe=P3),
    "CUSTOM_KEYWORD1_ATTRIBUTES": KEYWORD,
    "CUSTOM_KEYWORD2_ATTRIBUTES": a(P6, font=BOLD),
    "CUSTOM_KEYWORD3_ATTRIBUTES": a(P3, font=BOLD),
    "CUSTOM_KEYWORD4_ATTRIBUTES": a(MINT, font=BOLD),
    "INJECTED_LANGUAGE_FRAGMENT": a(bg="#081a0c"),
    "BOOKMARKS_ATTRIBUTES": a(stripe=P3),
    "INLAY_DEFAULT": a(P4, "#0c1a0d"),
    "INLAY_TEXT_WITHOUT_BACKGROUND": a(P4),
    "INLINE_PARAMETER_HINT": a(P4, "#0c1a0d"),
    "INLINE_PARAMETER_HINT_HIGHLIGHTED": a(P7, "#12301a"),
    "INLINE_PARAMETER_HINT_CURRENT": a(P7, SEL),
    "CODE_LENS_BORDER_COLOR": a(effect=DIM),
    "BREADCRUMBS_DEFAULT": a(P4),
    "BREADCRUMBS_HOVERED": a(P7, "#0f2614"),
    "BREADCRUMBS_CURRENT": a(FG, "#12301a"),
    "BREADCRUMBS_INACTIVE": a(DIM),

    # --- Debugger / coverage ---
    "BREAKPOINT_ATTRIBUTES": a(bg=ERROR_BG, stripe=ERROR),
    "EXECUTIONPOINT_ATTRIBUTES": a(P7, "#1f5a2c"),
    "NOT_TOP_FRAME_ATTRIBUTES": a(bg="#12301a"),
    "DEBUGGER_INLINED_VALUES": a(P4, font=ITALIC),
    "DEBUGGER_INLINED_VALUES_MODIFIED": a(P3, font=ITALIC),
    "DEBUGGER_INLINED_VALUES_EXECUTION_LINE": a(P6, font=ITALIC),
    "LINE_FULL_COVERAGE": a(P1),
    "LINE_PARTIAL_COVERAGE": a(WARNING),
    "LINE_NONE_COVERAGE": a(ERROR),

    # --- Diff / merge ---
    "DIFF_INSERTED": a(bg="#0f3d1c", stripe=P1),
    "DIFF_MODIFIED": a(bg="#1f3a10", stripe=P3),
    "DIFF_DELETED": a(bg="#2e1a08", stripe=DELETED),
    "DIFF_CONFLICT": a(bg="#3d2a08", stripe=ERROR),

    # --- Console / logs ---
    "CONSOLE_NORMAL_OUTPUT": a(FG),
    "CONSOLE_ERROR_OUTPUT": a(ERROR),
    "CONSOLE_SYSTEM_OUTPUT": a(P4),
    "CONSOLE_USER_INPUT": a(P7, font=ITALIC),
    "CONSOLE_RANGE_TO_EXECUTE": a(effect=P1, etype=BOXED),
    "LOG_ERROR_OUTPUT": a(ERROR),
    "LOG_WARNING_OUTPUT": a(WARNING),
    "LOG_INFO_OUTPUT": a(FG),
    "LOG_DEBUG_OUTPUT": a(P4),
    "LOG_VERBOSE_OUTPUT": a(DIM),
    "LOG_EXPIRED_ENTRY": a(DIM),

    # --- Go ---
    "GO_BUILTIN_CONSTANT": a(P6, font=BOLD),
    "GO_BUILTIN_FUNCTION_CALL": BUILTIN,
    "GO_BUILTIN_TYPE_REFERENCE": a(MINT, font=BOLD),
    "GO_BUILTIN_VARIABLE": BUILTIN,
    "GO_EXPORTED_FUNCTION_CALL": FUNC_CALL,
    "GO_LOCAL_FUNCTION_CALL": FUNC_CALL,
    "GO_METHOD_RECEIVER": a(FG, font=ITALIC),
    "GO_PACKAGE": PACKAGE,
    "GO_TYPE_REFERENCE": TYPE,
    "GO_COMMENT_REFERENCE": a(P5, font=ITALIC),
    "GO_SHADOWING_VARIABLE": a(FG, effect=WARNING, etype=UNDERSCORE),
    "GO_SYNTAX_UPDATE": a(effect=P6, etype=WAVE),
    "com.plan9.INSTRUCTION": KEYWORD,
    "com.plan9.PSEUDO_INSTRUCTION": a(P6),
    "com.plan9.REGISTER": a(P3),
    "com.plan9.LABEL": a(MINT),
    "com.plan9.IDENTIFIER": a(FG),

    # --- PHP ---
    "PHP_VAR": a(FG),
    "PHP_PARAMETER": PARAM,
    "PHP_INSTANCE_FIELD": FIELD,
    "PHP_STATIC_FIELD": a(P7, font=ITALIC),
    "PHP_CONSTANT": CONSTANT,
    "PHP_FUNCTION_CALL": FUNC_CALL,
    "PHP_METHOD_CALL": FUNC_CALL,
    "PHP_STATIC_METHOD_CALL": a(FG, font=ITALIC),
    "PHP_PREDEFINED_SYMBOL": BUILTIN,
    "PHP_TAG": a(P7, font=BOLD),
    "PHP_HEREDOC_ID": a(P3, font=BOLD),
    "PHP_HEREDOC_CONTENT": a(P3, "#081a0c"),
    "PHP_EXEC_COMMAND_ID": a(P3, "#081a0c"),
    "PHP_ESCAPE_SEQUENCE": a(P6, font=BOLD),
    "PHP_DOC_TAG": a(P5, font=BOLD_ITALIC),
    "PHP_DOC_PARAMETER": a(P5, font=ITALIC),
    "PHP_NAMED_ARGUMENT": a(P5),
    "PHP_ATTRIBUTE": METADATA,
    "PHP_SCRIPTING_BACKGROUND": a(bg=BG),
    "PHP_MARKUP_ID": a(P4),

    # --- JS / TS ---
    "JS.LOCAL_VARIABLE": a(FG),
    "JS.GLOBAL_VARIABLE": GLOBAL,
    "JS.GLOBAL_FUNCTION": FUNC_CALL,
    "JS.INSTANCE_MEMBER_FUNCTION": FUNC_CALL,
    "JS.INSTANCE_MEMBER_VARIABLE": FIELD,
    "JS.PARAMETER": PARAM,
    "JS.REGEXP": a(P6, "#081a0c"),
    "JS.JSX_CLIENT_COMPONENT": TYPE,
    "JavaScript:INJECTED_LANGUAGE_FRAGMENT": a(bg="#081a0c"),
    "TS.TYPE_GUARD": a(MINT, font=ITALIC),
    "TS.TYPE_PARAMETER": a(MINT, font=ITALIC),
    "Static method access": a(FG, font=ITALIC),
    "Static property reference ID": a(P7, font=ITALIC),

    # --- Markup / data formats ---
    "HTML_TAG": a(PUNCT),
    "HTML_TAG_NAME": TAG,
    "HTML_CUSTOM_TAG_NAME": a(MINT),
    "HTML_ATTRIBUTE_NAME": ATTR,
    "HTML_ATTRIBUTE_VALUE": STRING,
    "HTML_ENTITY_REFERENCE": a(P6, font=ITALIC),
    "XML_TAG": a(PUNCT),
    "XML_TAG_NAME": TAG,
    "XML_CUSTOM_TAG_NAME": a(MINT),
    "XML_ATTRIBUTE_NAME": ATTR,
    "XML_ATTRIBUTE_VALUE": STRING,
    "XML_ENTITY_REFERENCE": a(P6, font=ITALIC),
    "XML_PROLOGUE": a(P4),
    "CSS.COLOR": a(P6),
    "CSS.IMPORTANT": a(P7, font=BOLD),
    "CSS.URL": a(P3, effect=P3, etype=UNDERSCORE),
    "CSS.PROPERTY_NAME": ATTR,
    "CSS.TAG_NAME": TAG,
    "MARKDOWN_HEADER": a(P7, font=BOLD),
    "MARKDOWN_HEADER_LEVEL_1": a(P7, font=BOLD),
    "MARKDOWN_HEADER_LEVEL_2": a(P7, font=BOLD),
    "MARKDOWN_CODE_SPAN": a(P3),
    "MARKDOWN_CODE_BLOCK": a(P3),
    "MARKDOWN_LINK_TEXT": a(P6, effect=P6, etype=UNDERSCORE),
    "MARKDOWN_AUTO_LINK": a(P6, effect=P6, etype=UNDERSCORE),
    "MARKDOWN_IMAGE": a(P6),
    "MARKDOWN_BOLD": a(FG, font=BOLD),
    "MARKDOWN_ITALIC": a(FG, font=ITALIC),
    "MARKDOWN_BLOCK_QUOTE": a(P4, font=ITALIC),
    "YAML_ANCHOR": a(P6, font=ITALIC),
    "YAML_SCALAR_KEY": FIELD,
    "JSON.PROPERTY_KEY": FIELD,
    "PROPERTIES.KEY": FIELD,
    "PROPERTIES.INVALID_STRING_ESCAPE": a(ERROR, effect=ERROR, etype=WAVE),
    "REGEXP.CHAR_CLASS": a(P6),
    "REGEXP.REDUNDANT_ESCAPE": a(P4),
    "HTTP_REQUEST_PARAMETER_NAME": ATTR,
    "HTTP_REQUEST_PARAMETER_VALUE": STRING,
    "BASH.EXTERNAL_COMMAND": FUNC_CALL,
    "BASH.HERE_DOC_START": a(P3, font=BOLD),
    "BASH.HERE_DOC_END": a(P3, font=BOLD),
    "BASH.SHEBANG": COMMENT,
    "BASH.BINARY_DATA": a(DIM),
    "SQL_SYNTHETIC_ENTITY": a(P5, font=ITALIC),
    "SQL_OUTER_QUERY_COLUMN": a(P5),
    "GHERKIN_REGEXP_PARAMETER": a(P6),
    "JSP_DIRECTIVE_NAME": a(P7, font=BOLD),
    "QUTE_BACKGROUND": a(bg="#081a0c"),
    "KUBERNETES_POD_STATUS_ERROR": a(ERROR),
    "KUBERNETES_POD_STATUS_SUCCESS": a(P1),
    "KUBERNETES_POD_STATUS_OTHER": a(WARNING),
    "KOTLIN_MUTABLE_VARIABLE": a(FG, effect=DIM, etype=UNDERSCORE),
    "KOTLIN_NAMED_ARGUMENT": a(P5),
    "KOTLIN_LABEL": a(P3, font=ITALIC),
    "KOTLIN_SMART_CAST_VALUE": a(bg="#12301a"),
    "KOTLIN_SMART_CAST_RECEIVER": a(bg="#12301a"),
    "KOTLIN_SMART_CONSTANT": a(bg="#12301a"),
}

for name, color in ANSI.items():
    ATTRS[f"CONSOLE_{name}_OUTPUT"] = a(color)


def hx(color):
    return color.lstrip("#")


def scheme_xml():
    out = ['<scheme name="Wasteland Terminal" version="142" parent_scheme="Darcula">',
           "  <metaInfo>",
           '    <property name="created">2026-11-02T00:00:00</property>',
           '    <property name="ide">idea</property>',
           '    <property name="ideVersion">2026.1.0.0</property>',
           '    <property name="originalScheme">Wasteland Terminal</property>',
           "  </metaInfo>",
           "  <colors>"]
    for name, color in sorted(SCHEME_COLORS.items()):
        out.append(f"    <option name={quoteattr(name)} value=\"{hx(color)}\" />")
    out += ["  </colors>", "  <attributes>"]
    for name, spec in sorted(ATTRS.items()):
        out.append(f"    <option name={quoteattr(name)}>")
        out.append("      <value>")
        for key in ("FOREGROUND", "BACKGROUND", "FONT_TYPE", "ERROR_STRIPE_COLOR",
                    "EFFECT_COLOR", "EFFECT_TYPE"):
            v = spec[key]
            if v is None:
                continue
            v = hx(v) if isinstance(v, str) else str(v)
            out.append(f"        <option name=\"{key}\" value=\"{v}\" />")
        out.append("      </value>")
        out.append("    </option>")
    out += ["  </attributes>", "</scheme>", ""]
    return "\n".join(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "WastelandTerminal.theme.json").write_text(json.dumps(theme_json(), indent=2) + "\n")
    (OUT / "WastelandTerminalCRT.theme.json").write_text(
        json.dumps(theme_json(crt=True), indent=2) + "\n")
    (OUT / "WastelandTerminal.xml").write_text(scheme_xml())
    (OUT / SCANLINES_FILE).write_bytes(scanlines_png())
    print(f"Wrote 2 UI themes, the editor scheme and {SCANLINES_FILE} to {OUT}")


if __name__ == "__main__":
    main()
