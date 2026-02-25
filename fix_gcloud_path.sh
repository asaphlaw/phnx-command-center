#!/bin/bash
# Fix gcloud path

export PATH="$PATH:$HOME/google-cloud-sdk/bin"

echo "✅ gcloud path fixed for this session!"
echo ""
echo "You can now run:"
echo "  gcloud auth application-default login"
echo ""
echo "Or restart your terminal to make this permanent."
