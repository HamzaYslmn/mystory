import { create } from 'zustand';

// MARK: - Editing flag (dev-only).
// True while a chapter is being edited so the Reader can hide its toolbar
// and ignore tap-to-toggle while focus may be on the editor inputs.
interface EditingStore {
  editing: boolean;
  setEditing: (v: boolean) => void;
}

export const useEditingStore = create<EditingStore>((set) => ({
  editing: false,
  setEditing: (editing) => set({ editing }),
}));
