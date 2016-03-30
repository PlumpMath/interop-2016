#!/usr/bin/env bash


find . -type f -iname "*.yml" -print0 | while IFS= read -r -d $'\0' line; do
    yamllint "$line" || exit   
    
done
