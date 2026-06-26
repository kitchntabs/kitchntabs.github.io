
# Dash Dialog Component

The `dash-dialog` package provides a simple, imperative API for displaying confirmation dialogs in React applications.

---

## Installation

The package is already included in the dash-frontend monorepo.

---

## Basic Usage

```tsx
import { useDialog } from "dash-dialog";

const MyComponent = () => {
    const dialog = useDialog();
    
    const handleAction = () => {
        dialog({
            variant: "info",
            title: "Confirm Action",
            content: "Are you sure you want to proceed?",
            showCancelButton: true,
            onConfirm: () => {
                // Handle confirm action
                console.log("Confirmed!");
            },
            onCancel: () => {
                // Handle cancel action (optional)
                console.log("Cancelled");
            }
        });
    };
    
    return <button onClick={handleAction}>Delete Item</button>;
};
```

---

## API Reference

### `useDialog()`

Returns a `dialog` function that accepts a configuration object.

### Configuration Options

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `variant` | `"info" \| "danger" \| "warning" \| "success"` | Yes | Dialog style variant |
| `title` | `string` | Yes | Dialog title |
| `content` | `string \| ReactNode` | Yes | Dialog body content |
| `showCancelButton` | `boolean` | No | Show cancel button (default: false) |
| `onConfirm` | `() => void` | No | Callback when user confirms |
| `onCancel` | `() => void` | No | Callback when user cancels |
| `confirmText` | `string` | No | Custom confirm button text |
| `cancelText` | `string` | No | Custom cancel button text |

---

## Variants

### Info (Blue)
```tsx
dialog({
    variant: "info",
    title: "Information",
    content: "This is an informational message."
});
```

### Danger (Red)
```tsx
dialog({
    variant: "danger",
    title: "Delete Item",
    content: "This action cannot be undone. Are you sure?",
    showCancelButton: true,
    onConfirm: () => deleteItem()
});
```

### Warning (Orange)
```tsx
dialog({
    variant: "warning",
    title: "Warning",
    content: "This may have unintended consequences."
});
```

### Success (Green)
```tsx
dialog({
    variant: "success",
    title: "Success",
    content: "Operation completed successfully!"
});
```

---

## Common Patterns

### Delete Confirmation
```tsx
const handleDelete = (item: Item) => {
    dialog({
        variant: "danger",
        title: translate("dialog.delete.title", { _: "Delete Item" }),
        content: translate("dialog.delete.content", {
            name: item.name,
            _: `Are you sure you want to delete "${item.name}"?`
        }),
        showCancelButton: true,
        onConfirm: async () => {
            await dataProvider.delete(resource, { id: item.id });
            refresh();
            notify("Item deleted", { type: "success" });
        }
    });
};
```

### Batch Actions
```tsx
const handleBatchDelete = (selectedIds: number[]) => {
    dialog({
        variant: "danger",
        title: "Delete Selected Items",
        content: `Are you sure you want to delete ${selectedIds.length} items?`,
        showCancelButton: true,
        onConfirm: async () => {
            await Promise.all(
                selectedIds.map(id => dataProvider.delete(resource, { id }))
            );
            refresh();
        }
    });
};
```

### Status Change Confirmation
```tsx
const handleStatusChange = (item: Item, newStatus: string) => {
    dialog({
        variant: "info",
        title: "Change Status",
        content: `Change status of "${item.name}" to "${newStatus}"?`,
        showCancelButton: true,
        onConfirm: async () => {
            await updateStatus(item.id, newStatus);
            refresh();
        }
    });
};
```

---

## Integration with Loading States

Use with `dash-global-loader` for async operations:

```tsx
const handleAsyncAction = () => {
    dialog({
        variant: "info",
        title: "Process Items",
        content: "This may take a moment. Continue?",
        showCancelButton: true,
        onConfirm: async () => {
            // Show global loader
            window.dispatchEvent(
                new MessageEvent('dash-global-loader', { data: true })
            );
            
            try {
                await processItems();
                refresh();
            } finally {
                // Hide global loader
                window.dispatchEvent(
                    new MessageEvent('dash-global-loader', { data: false })
                );
            }
        }
    });
};
```

---

## Source Files

- Package: `packages/dash-dialog/`
- Example usage: [CampaignProductsBatchActions.tsx](file:///Users/farandal/DASH-PW-PROJECT/dash-frontend/packages/kt-ecommerce/src/components/Campaign/Campaign/CampaignProductsBatchActions.tsx)
