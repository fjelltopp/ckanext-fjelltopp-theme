#!/bin/sh

SINGULAR_OLD_TERM="$1"
PLURAL_OLD_TERM="$2"
SINGULAR_TERM="$3"
PLURAL_TERM="$4"
LOCALE="$5"

# build po/mo files

LC_FILES_DIR="ckanext/fjelltopp_theme/i18n/$LOCALE/LC_MESSAGES"
PO_FILE="$LC_FILES_DIR/ckanext-fjelltopp-theme.po"
MO_FILE="$LC_FILES_DIR/ckanext-fjelltopp-theme.mo"

# Remove existing PO file if it exists
if [ -f "$PO_FILE" ]; then
    echo "Removing existing PO file..."
    rm "$PO_FILE" || {
        echo "Error: Failed to remove existing PO file"
        exit 1
    }
fi

# Initialize new catalog
echo "Initializing translation catalog..."
python setup.py init_catalog --locale $LOCALE || {
    echo "Error: Failed to initialize catalog"
    exit 1
}

# Verify PO file was created
if [ ! -f "$PO_FILE" ]; then
    echo "Error: PO file was not created"
    exit 1
fi

# Process the translations
echo "Processing translations..."
python "term_changer.py" "$PO_FILE" "$SINGULAR_OLD_TERM" "$PLURAL_OLD_TERM" "$SINGULAR_TERM" "$PLURAL_TERM" || {
    echo "Error: Failed to process translations"
    exit 1
}

# Remove existing MO file if it exists
if [ -f "$MO_FILE" ]; then
    echo "Removing existing MO file..."
    rm "$MO_FILE" || {
        echo "Error: Failed to remove existing MO file"
        exit 1
    }
fi

# Compile the catalog
echo "Compiling..."
python setup.py compile_catalog || {
    echo "Error: Failed to compile catalog"
    exit 1
}

# Verify MO file was created
if [ ! -f "$MO_FILE" ]; then
    echo "Error: MO file was not created"
    exit 1
fi
echo "Translation catalog successfully updated and compiled"