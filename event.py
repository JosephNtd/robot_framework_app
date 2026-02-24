from PyQt5.QtCore import Qt

class Event():
    """
    Handle all event interaction from user
    """
    def __init__(self, parent):
        self.parent = parent
        self._updating = False

    def on_item_changed(self, item) -> None:
        """
        Update check box state from test case by recursion
        If parent checked -> checked all children too
        If parent unchecked -> unchecked all children too
        If not all children checked -> partially checked parent
        If not any children checked -> parent unchecked
        """
        if self._updating:
            return

        self._updating = True

        state = item.checkState()
        self.update_children(item, state)
        self.update_parent(item)

        self._updating = False

    def update_children(self, item, state) -> None:
        """
        Update check state for children base on parent check state
        if the children have children inside it -> set check state them too
        """
        for row in range(item.rowCount()):
            child = item.child(row)
            child.setCheckState(state)
            self.update_children(child, state)

    def update_parent(self, item) -> None:
        """
        Update check state for parent base on children check state
        if the parent is other children -> update the grand too
        """
        
        #  If the current node is root -> stop
        parent = item.parent()
        if not parent:
            return

        # Count the checked one and unchecked one the set check state for parent
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

    def on_clicked_row_tree(self, index) -> None:
        """
        Check the check box when user click the row
        Don't need to specifically click the check box
        """
        item = self.parent.model.itemFromIndex(index)
        if item and item.isCheckable():
            new_state = Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked
            item.setCheckState(new_state)
