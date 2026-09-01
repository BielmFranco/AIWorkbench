#!/usr/bin/env sh
set -eu

target="${1:-}"
skill="${2:-all}"
install_path="${3:-}"
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname "$script_dir")
source_root="$repo_root/skills"

case "$target" in
  codex) destination_root="${CODEX_HOME:-$HOME/.codex}/skills" ;;
  claude) destination_root="$HOME/.claude/skills" ;;
  *) echo "Uso: $0 codex|claude [all|nome-da-skill]" >&2; exit 2 ;;
esac
if [ -n "$install_path" ]; then destination_root="$install_path"; fi

[ -d "$source_root" ] || { echo "Diretório não encontrado: $source_root" >&2; exit 1; }
mkdir -p "$destination_root"
count=0

install_one() {
  source="$source_root/$1"
  [ -f "$source/SKILL.md" ] || { echo "Skill desconhecida: $1" >&2; exit 1; }
  destination="$destination_root/$1"
  mkdir -p "$destination"
  cp -R "$source/." "$destination/"
  printf 'Instalada: %s -> %s\n' "$1" "$destination"
  count=$((count + 1))
}

if [ "$skill" = "all" ]; then
  for directory in "$source_root"/*; do
    [ -d "$directory" ] || continue
    install_one "$(basename "$directory")"
  done
else
  install_one "$skill"
fi

printf 'Concluído: %s skill(s) instalada(s) para %s.\n' "$count" "$target"
