#!/usr/bin/env python
import os
import re
import sys
import zipfile

def build_skill(plugin_dir, output_path):
    plugin_name = os.path.basename(plugin_dir.rstrip('/\\'))

    meta_file = os.path.join(plugin_dir, 'skill.yaml')
    if not os.path.exists(meta_file):
        print(f"Skipping {plugin_name} - no skill.yaml found", file=sys.stderr)
        return

    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = f.read()

    name_match = re.search(r'^name:\s*(.+)$', meta, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+)$', meta, re.MULTILINE)
    skill_name = name_match.group(1).strip() if name_match else plugin_name
    skill_desc = desc_match.group(1).strip() if desc_match else ''

    with open(os.path.join(plugin_dir, 'instructions.md'), 'r', encoding='utf-8') as f:
        instructions = f.read()

    skill_md = "---\nname: {}\ndescription: {}\n---\n\n{}".format(skill_name, skill_desc, instructions)

    exclude = {'instructions.md', 'skill.yaml', 'README.md'}

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('{}/SKILL.md'.format(plugin_name), skill_md.encode('utf-8'))
        for root, dirs, files in os.walk(plugin_dir):
            dirs.sort()
            for fname in sorted(files):
                if root == plugin_dir and fname in exclude:
                    continue
                fpath = os.path.join(root, fname)
                arcname = '{}/{}'.format(plugin_name, os.path.relpath(fpath, plugin_dir).replace('\\', '/'))
                zf.write(fpath, arcname)

    print("Created {}".format(output_path))

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    claude_ai_dir = os.path.join(repo_root, 'claude-ai')

    for entry in sorted(os.listdir(claude_ai_dir)):
        plugin_dir = os.path.join(claude_ai_dir, entry)
        if os.path.isdir(plugin_dir):
            build_skill(plugin_dir, os.path.join(claude_ai_dir, '{}.skill'.format(entry)))
