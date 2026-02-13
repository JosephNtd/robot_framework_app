from PyQt5.QtCore import Qt

class Event():
    def __init__(self, parent):
        self.parent = parent
        self._updating = False

    def on_item_changed(self, item):
        if self._updating:
            return

        self._updating = True

        state = item.checkState()
        self.update_children(item, state)
        self.update_parent(item)

        self._updating = False

    def update_children(self, item, state):
        for row in range(item.rowCount()):
            child = item.child(row)
            child.setCheckState(state)
            self.update_children(child, state)

    def update_parent(self, item):
        parent = item.parent()
        if not parent:
            return

        checked_count = 0
        unchecked_count = 0

        for row in range(parent.rowCount()):
            child = parent.child(row)
            if child.checkState() == Qt.Checked:
                checked_count += 1
            else:
                unchecked_count += 1

        if checked_count == parent.rowCount():
            parent.setCheckState(Qt.Checked)
        elif unchecked_count == parent.rowCount():
            parent.setCheckState(Qt.Unchecked)
        else:
            parent.setCheckState(Qt.PartiallyChecked)

        self.update_parent(parent)

    def on_clicked_row_tree(self, index):
        item = self.parent.model.itemFromIndex(index)
        if item and item.isCheckable():
            new_state = Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked
            item.setCheckState(new_state)
