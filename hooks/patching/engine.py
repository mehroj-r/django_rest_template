from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from pathlib import Path
from typing import Callable, Sequence

from .ops import FilePatcher


class PatchEngineError(RuntimeError):
    pass


@dataclass(frozen=True)
class PatchSpec:
    patch_id: str
    apply: Callable[[FilePatcher], None]
    priority: int = 100
    after: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


class PatchEngine:
    def __init__(self, project_root: Path):
        self.patcher = FilePatcher(project_root)

    def run(self, patches: Sequence[PatchSpec]) -> list[str]:
        ordered = self.order_patches(patches)
        selected_ids = {patch.patch_id for patch in ordered}

        for patch in ordered:
            conflicts = sorted(set(patch.conflicts) & selected_ids)
            if conflicts:
                raise PatchEngineError(f"Patch {patch.patch_id} conflicts with: {', '.join(conflicts)}")

        applied: list[str] = []
        for patch in ordered:
            patch.apply(self.patcher)
            applied.append(patch.patch_id)

        return applied

    @staticmethod
    def order_patches(patches: Sequence[PatchSpec]) -> list[PatchSpec]:
        patch_by_id: dict[str, PatchSpec] = {}
        for patch in patches:
            if patch.patch_id in patch_by_id:
                raise PatchEngineError(f"Duplicate patch id: {patch.patch_id}")
            patch_by_id[patch.patch_id] = patch

        graph: dict[str, set[str]] = {patch.patch_id: set() for patch in patches}
        indegree: dict[str, int] = {patch.patch_id: 0 for patch in patches}

        for patch in patches:
            for dependency in patch.after:
                if dependency not in patch_by_id:
                    raise PatchEngineError(f"Patch {patch.patch_id} requires unknown dependency {dependency}")
                if patch.patch_id in graph[dependency]:
                    continue
                graph[dependency].add(patch.patch_id)
                indegree[patch.patch_id] += 1

        queue: list[tuple[int, str]] = []
        for patch in patches:
            if indegree[patch.patch_id] == 0:
                heappush(queue, (patch.priority, patch.patch_id))

        ordered_ids: list[str] = []
        while queue:
            _, patch_id = heappop(queue)
            ordered_ids.append(patch_id)

            for child in sorted(graph[patch_id]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    child_patch = patch_by_id[child]
                    heappush(queue, (child_patch.priority, child_patch.patch_id))

        if len(ordered_ids) != len(patches):
            raise PatchEngineError("Patch ordering failed: cyclic dependency detected")

        return [patch_by_id[patch_id] for patch_id in ordered_ids]
