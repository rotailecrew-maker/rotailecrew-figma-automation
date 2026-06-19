# -*- coding: utf-8 -*-
import json, requests

fk = "unsaved-mqkseo9k-wm8q0x3r"
BASE = "http://localhost:1994/rpc"

def rpc(tool, node_ids, params=None):
    p = {"tool": tool, "nodeIds": node_ids, "fileKey": fk}
    if params:
        p["params"] = params
    r = requests.post(BASE, headers={"Content-Type": "application/json"},
                      data=json.dumps(p).encode("utf-8"), timeout=15)
    return r.json().get("data")

def find_text_nodes(node, depth=0):
    prefix = "  " * depth
    t = node.get("type", "")
    name = node.get("name", "")
    nid = node.get("id", "")
    if t == "TEXT":
        chars = node.get("characters", "")
        turkce = {0x131,0x130,0xFC,0xF6,0x15F,0x11F,0xE7,0x11E,0xD6,0xDC,0x15E,0xC7}
        tr_count = sum(1 for c in chars if ord(c) in turkce)
        print(f"{prefix}[TEXT] id={nid} | tr={tr_count} | {repr(chars[:60])}")
    else:
        print(f"{prefix}[{t}] {name} | id={nid}")
    for child in node.get("children", []):
        find_text_nodes(child, depth + 1)

node = rpc("get_node", ["933:2"])
print("=== Post 308 (Kapak) ===")
find_text_nodes(node)
