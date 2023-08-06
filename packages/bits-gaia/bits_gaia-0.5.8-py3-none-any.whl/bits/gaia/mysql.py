# -*- coding: utf-8 -*-
"""MySQL class file."""
import json
import logging

from bits.mysql import MySQL as BITSMySQL


class MySQL(BITSMySQL):
    """MySQL Class."""

    def __init__(self, server, port, user, password, db, verbose=False):
        """Initialize an MySQL class instance."""
        BITSMySQL.__init__(self, server, port, user, password, db, verbose)

    def display_changes(self, old_items, new_items):
        """Return the text output of the changes for the collection."""
        changes = {}
        for key in new_items:
            if key not in old_items:
                continue
            new = new_items[key]
            old = old_items[key]
            output = []
            for k in sorted(new):
                n = new[k]
                o = old.get(k)
                if n != o:
                    output.append(f"  {k}: {json.dumps(o, default=str)} -> {json.dumps(n, default=str)}")
            changes[key] = output
        return changes

    def find_items_to_add(self, old_items, new_items):
        """Return a list of items to add to the database."""
        add = []
        for key in new_items:
            new = new_items[key]
            if key not in old_items:
                add.append(new)
        return add

    def find_items_to_delete(self, old_items, new_items):
        """Return a list of items to delete from the database."""
        delete = []
        for key in old_items:
            old = old_items[key]
            if key not in new_items:
                delete.append(old)
        return delete

    def find_items_to_update(self, old_items, new_items):
        """Return a list of items to update in the database."""
        update = []
        for key in new_items:
            new = new_items[key]
            if key not in old_items:
                continue
            old = old_items[key]
            has_updates = False
            for k in sorted(new):
                n = new[k]
                o = old.get(k)
                if n != o:
                    has_updates = True
                    break
            if has_updates:
                update.append(new)
        return update

    #
    # Database changes (add, delete, update)
    #
    def add_records(self, kind, index_key, name_key, query, records):
        """Add records to the database."""
        if not records:
            return
        cur = self.create_dictcursor()

        for record in sorted(records, key=lambda x: x[name_key] if x[name_key] else ""):
            name = record[name_key]
            try:
                cur.execute(query, record)
                index = cur.lastrowid
                print(f" + {name} [{index}]")
            except Exception as err:
                logging.error(f"Failed to insert {kind}: {record} [{err}]")
            self.db.commit()
        cur.close()

    def delete_records(self, kind, index_key, name_key, query, records):
        """Delete records from the database."""
        if not records:
            return
        cur = self.create_dictcursor()

        for record in sorted(records, key=lambda x: x[name_key] if x[name_key] else ""):
            index = record[index_key] if index_key in record else None
            name = record[name_key]
            try:
                cur.execute(query, record)
                if index:
                    print(f" - {name} [{index}]")
                else:
                    print(f" - {name}")
            except Exception as err:
                logging.error(f"Failed to delete {kind}: {record} [{err}]")
            self.db.commit()
        cur.close()

    def update_records(self, kind, index_key, name_key, query, records, changes):
        """Update records in the database."""
        if not records:
            return
        cur = self.create_dictcursor()
        for record in sorted(records, key=lambda x: x[name_key] if x[name_key] else ""):
            index = record[index_key] if index_key in record else None
            name = record[name_key]
            try:
                cur.execute(query, record)
                if index:
                    print(f" * {name} [{index}]")
                else:
                    print(f" * {name}")
                if index and index in changes:
                    print("  " + "\n  ".join(changes[index]))
            except Exception as err:
                logging.error(f"Failed to update {kind}: {record} [{err}]")
                print(query)
            self.db.commit()
        cur.close()

    def update_table(
        self,
        kind,
        old_items,
        new_items,
        index_key,
        name_key,
        add_query,
        delete_query,
        update_query,
    ):
        """Update a single table in a MySQL Database."""
        print(f"\nUpdating {len(new_items)} {kind} records in MySQL...")
        add = self.find_items_to_add(old_items, new_items)
        delete = self.find_items_to_delete(old_items, new_items)
        update = self.find_items_to_update(old_items, new_items)
        changes = self.display_changes(old_items, new_items)
        if add:
            print(f"\nAdding {len(add)} {kind} records...")
            self.add_records(kind, index_key, name_key, add_query, add)
        if delete:
            print(f"\nDeleting {len(delete)} {kind} records...")
            self.delete_records(kind, index_key, name_key, delete_query, delete)
        if update:
            print(f"\nUpdating {len(update)} {kind} records...")
            self.update_records(kind, index_key, name_key, update_query, update, changes)
        return changes
