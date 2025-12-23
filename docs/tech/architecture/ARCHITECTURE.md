# Dash Auto Admin Architecture Documentation

## Overview

The **dash-auto-admin** package is the core rendering engine of the Dash Framework's frontend. It interprets resource configurations and schemas to automatically generate CRUD interfaces using React Admin as its foundation. This document explores the interconnections between components, from high-level resource definitions to low-level field rendering.

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Component Hierarchy](#component-hierarchy)
3. [Resource Configuration Flow](#resource-configuration-flow)
4. [Schema Interpretation](#schema-interpretation)
5. [Context Component System](#context-component-system)
6. [Mode-Based Rendering](#mode-based-rendering)
7. [Custom Component Integration](#custom-component-integration)
8. [Key Interfaces](#key-interfaces)

---

## Core Concepts

### 1. Resource Configuration (`IDashAutoAdminResourceConfig`)

A Resource Configuration defines everything about a CRUD resource:
- API endpoint (`model`)
- UI presentation (icons, labels, menus)
- Schema (field definitions)
- Behavior (drawer modes, redirects, mutations)
- Context wrapping (`contextComponent`)

### 2. Schema (`IDashAutoAdminAttribute[]`)

A Schema is an array of attribute definitions that describe:
- Field names and types
- Visibility per mode (list, create, edit, show)
- Custom components
- Grouping (tabs, groups, layouts)

### 3. Modes

The system operates in four primary modes:
- **list**: Datagrid/table view
- **create**: New record form
- **edit**: Update existing record form
- **show/view**: Read-only display

---

## Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                        DASHResources.tsx                        │
│            (Array of IDashAutoAdminResourceConfig)              │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ResourceTemplate.tsx                        │
│              (dash-admin template wrapper)                       │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DashAutoResource.tsx                         │
│         (Routes: List, Create, Edit, Show endpoints)             │
└─────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  DashAutoList   │   │ DashAutoCreate  │   │  DashAutoEdit   │
│                 │   │ DashAutoShow    │   │                 │
└─────────────────┘   └─────────────────┘   └─────────────────┘
           │                     │                     │
           ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DashAutoTabbedForm.tsx                        │
│              (Form rendering with context support)               │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ContextComponent Wrapper                        │
│    (Optional: TabManagerProvider, or custom contexts)            │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              Schema Interpretation Layer                         │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│    │ DashAutoTabs │  │ AutoGroup    │  │ AutoLayout   │        │
│    └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              Field/Input Rendering                               │
│    ┌────────────────┐         ┌────────────────┐               │
│    │AttributeToInput│ (forms) │AttributeToField│ (display)     │
│    └────────────────┘         └────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              UserAction.tsx (Custom Component Wrapper)           │
│    Renders custom components with method, attribute, record      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Resource Configuration Flow

### Step 1: Define Resources in `DASHResources.tsx`

```tsx
// apps/dash/src/DASHResources.tsx
import tabResource from './resources/tabResource';
import userResource from './resources/userResource';

export const DASHResources = [
    ...tabResource,
    ...userResource,
    // ... other resources
];
```

### Step 2: Resource Configuration Structure

```tsx
// apps/dash/src/resources/tabResource.tsx
const tabResource: IDashAutoAdminResourceConfig[] = [
    {
        // Identification
        model: "tab/tab",           // API endpoint: /api/tab/tab
        group: "Tabs",              // Menu grouping
        label: "Tabs",              // Display name
        
        // Access Control
        roles: ["System", "Tenant", "Staff"],
        
        // Template & Schema
        component: ResourceTemplate,
        schema: tabSchema,          // Field definitions
        
        // Context Provider (KEY FEATURE)
        contextComponent: TabsContext,
        
        // Form Configuration
        formGroupMode: "layout",    // "tabs" | "groups" | "layout"
        
        // Drawer Behavior
        drawer: true,
        drawerOptions: {
            edit: false,
            create: false,
            show: true
        },
        
        // Redirects & Mutations
        mutationMode: "pessimistic",
        redirectAfterCreate: "edit",
        redirectAfterUpdate: "edit",
        
        // Custom Layouts
        editLayout(render) {
            return (
                <Grid container>
                    <Grid size={6}>{render("Productos")}</Grid>
                    <Grid size={6}>{render("Comanda")}</Grid>
                </Grid>
            );
        }
    }
];
```

### Step 3: Resource Loading in Dash Admin

```tsx
// packages/dash-admin/src/DashAdmin.tsx
function DashAdmin({ resources }) {
    return (
        <Admin>
            {resources.map(resourceConfig => (
                <Resource
                    key={resourceConfig.model}
                    name={resourceConfig.model}
                    list={<DashAutoResource resourceConfig={resourceConfig} />}
                    // ... create, edit, show
                />
            ))}
        </Admin>
    );
}
```

---

## Schema Interpretation

### Schema Definition

```tsx
// apps/dash/src/schemas/tab/tabSchema.tsx
const tabSchema: IDashAutoAdminAttribute[] = [
    {
        attribute: 'ai_toolbar',        // Field name
        tab: 'Productos',               // Tab grouping
        label: '',                       // Display label
        type: String,                   // Data type
        
        // Visibility flags
        inCreate: true,
        inEdit: true,
        inList: false,
        inShow: false,
        
        // Custom component
        custom: true,
        component: TabAgentToolbar,
        componentProps: {
            config: { enableVoice: true }
        }
    },
    {
        attribute: 'products',
        tab: 'Productos',
        label: 'Productos',
        type: Array,
        inCreate: true,
        inEdit: true,
        inList: false,
        inShow: false,
        custom: true,
        component: TabOrderProductsSelector,
    },
    {
        attribute: 'status',
        tab: 'Datos',
        label: 'Estado',
        type: String,
        inCreate: false,
        inEdit: true,
        inList: true,
        inShow: true,
    }
];
```

### Schema Processing Pipeline

```
Schema Array
     │
     ▼
┌─────────────────────────────────────────┐
│ groupByTabs(schema)                      │
│ Groups attributes by 'tab' property      │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Filter by mode (inCreate, inEdit, etc.) │
│ Only include attributes for current mode │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ AttributeToInput (forms) OR             │
│ AttributeToField (display)               │
└─────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Type Resolution:                         │
│ - String → TextInput / TextField         │
│ - Number → NumberInput / NumberField     │
│ - Boolean → BooleanInput / BooleanField  │
│ - Date → DateInput / DateField           │
│ - custom: true → UserAction wrapper      │
└─────────────────────────────────────────┘
```

### Form Group Modes

The `formGroupMode` property determines how schema attributes are organized:

#### 1. Tabs Mode (`formGroupMode: "tabs"`)
```tsx
// Renders attributes grouped by 'tab' property in tabbed interface
<TabbedForm>
    <Tab label="Productos">
        {/* attributes with tab: 'Productos' */}
    </Tab>
    <Tab label="Datos">
        {/* attributes with tab: 'Datos' */}
    </Tab>
</TabbedForm>
```

#### 2. Groups Mode (`formGroupMode: "groups"`)
```tsx
// Renders attributes in collapsible/expandable groups
<Accordion>
    <AccordionSummary>Productos</AccordionSummary>
    <AccordionDetails>{/* attributes */}</AccordionDetails>
</Accordion>
```

#### 3. Layout Mode (`formGroupMode: "layout"`)
```tsx
// Uses custom layout functions: createLayout, editLayout, showLayout
// The render() function receives tab name and returns those fields
editLayout(render) {
    return (
        <Grid container>
            <Grid size={6}>{render("Productos")}</Grid>
            <Grid size={6}>{render("Comanda")}</Grid>
        </Grid>
    );
}
```

---

## Context Component System

### Purpose

The `contextComponent` allows wrapping form/show content with custom React Context providers. This is essential for:
- Sharing state between schema components
- Providing hooks to custom components
- Managing complex form state (e.g., shopping cart, order management)

### How It Works

#### 1. Define Context Component

```tsx
// apps/dash/src/components/tab/Tab/TabContext.tsx
export const TabsContext: IDashAutoAdminResourceConfig["contextComponent"] = (props) => {
    const { children, mode } = props;
    const tab = useRecordContext<ITab>();

    // Different behavior per mode
    if (mode === "list") {
        return <TabsListProvider>{children}</TabsListProvider>;
    }

    // Wrap in TabManagerProvider for create/edit/show
    return (
        <TabManagerProvider
            tab={tab}
            productsResource="ecommerce/product"
            method={mode}
        >
            {children}
        </TabManagerProvider>
    );
};
```

#### 2. Configure in Resource

```tsx
const tabResource = {
    model: "tab/tab",
    contextComponent: TabsContext,  // ← Applied here
    schema: tabSchema,
};
```

#### 3. Usage in DashAutoTabbedForm (Create/Edit)

```tsx
// packages/dash-auto-admin/src/DashAutoTabbedForm.tsx
const DashAutoTabbedForm = ({ resourceConfig, mode }) => {
    // Get context or passthrough
    const ContextComponent = resourceConfig.contextComponent 
        ? resourceConfig.contextComponent 
        : ({ children }) => children;

    return (
        <SimpleForm>
            <ContextComponent mode={mode} resourceConfig={resourceConfig}>
                {/* Form fields rendered here */}
                {renderFormContent()}
            </ContextComponent>
        </SimpleForm>
    );
};
```

#### 4. Usage in DashAutoShow (Show/View)

```tsx
// packages/dash-auto-admin/src/DashAutoShow.tsx
const DashAutoShow = ({ resourceConfig }) => {
    const ContextComponent = resourceConfig.contextComponent 
        ? resourceConfig.contextComponent 
        : ({ children }) => <>{children}</>;

    return (
        <Show>
            <ContextComponent mode="show" resourceConfig={resourceConfig}>
                {/* Show content rendered here */}
                {DashAutoTabs(resourceConfig)}
            </ContextComponent>
        </Show>
    );
};
```

### Context Component Props

```typescript
interface ContextComponentProps {
    mode: 'list' | 'create' | 'edit' | 'show';
    resourceConfig: IDashAutoAdminResourceConfig;
    children: React.ReactNode;
}
```

### Mode Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Navigation                               │
└─────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
   /tab/tab              /tab/tab/1/edit        /tab/tab/1/show
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ DashAutoList │      │ DashAutoEdit │      │ DashAutoShow │
└──────────────┘      └──────────────┘      └──────────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ContextComponent    │ContextComponent    │ContextComponent
│ mode="list"  │      │ mode="edit"  │      │ mode="show"  │
└──────────────┘      └──────────────┘      └──────────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│TabsListProvider│    │TabManagerProvider│  │TabManagerProvider
│(no provider)  │     │(full context) │     │(full context) │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## Mode-Based Rendering

### AttributeToInput (Forms: Create/Edit)

Converts schema attributes to form inputs:

```tsx
// packages/dash-auto-admin/src/mui/AttributeToInput.tsx
export const AttributeToInput = (
    mode: 'create' | 'edit',
    resourceConfig: IDashAutoAdminResourceConfig,
    attribute: IDashAutoAdminAttribute,
) => {
    // Custom component
    if (attribute.custom && attribute.component) {
        return (
            <attribute.component
                method={mode}
                attribute={attribute}
                resourceConfig={resourceConfig}
                {...attribute.componentProps}
            />
        );
    }

    // Standard type mapping
    switch (attribute.type) {
        case String:
            return <TextInput source={attribute.attribute} label={attribute.label} />;
        case Number:
            return <NumberInput source={attribute.attribute} label={attribute.label} />;
        case Boolean:
            return <BooleanInput source={attribute.attribute} label={attribute.label} />;
        case Date:
            return <DateTimeInput source={attribute.attribute} label={attribute.label} />;
        // ... more types
    }
};
```

### AttributeToField (Display: List/Show)

Converts schema attributes to display fields:

```tsx
// packages/dash-auto-admin/src/mui/AttributeToField.tsx
export const AttributeToField = (
    method: 'view' | 'list',
    resourceConfig: IDashAutoAdminResourceConfig,
    attribute: IDashAutoAdminAttribute,
) => {
    // Custom component via UserAction wrapper
    if (attribute.custom && attribute.component) {
        return (
            <FunctionField
                render={(record) => (
                    <UserAction
                        method={method}
                        attribute={attribute}
                        resourceConfig={resourceConfig}
                        record={record}
                    />
                )}
            />
        );
    }

    // Standard type mapping
    switch (attribute.type) {
        case String:
            return <TextField source={attribute.attribute} label={attribute.label} />;
        case Number:
            return <NumberField source={attribute.attribute} label={attribute.label} />;
        case Boolean:
            return <BooleanField source={attribute.attribute} label={attribute.label} />;
        // ... more types
    }
};
```

---

## Custom Component Integration

### UserAction Wrapper

The `UserAction` component is the bridge between dash-auto-admin and custom components:

```tsx
// packages/dash-auto-admin/src/wrappers/UserAction.tsx
const UserAction: React.FC<IDashAutoAdminCustomFieldComponent> = ({ 
    method, 
    attribute, 
    resourceConfig, 
    record 
}) => {
    if (attribute.component && isFC(attribute.component)) {
        const Action = attribute.component as React.FC<IDashAutoAdminCustomFieldComponent>;
        
        return (
            <Action
                method={method}              // 'list', 'view', 'edit', 'create'
                attribute={attribute}        // Full attribute config
                resourceConfig={resourceConfig}
                record={record}              // Current record data
                {...attribute.componentProps}
            />
        );
    }
    
    return null;
};
```

### Custom Component Contract

All custom components receive standardized props:

```typescript
// packages/dash-auto-admin/src/interfaces/IDashAutoAdminCustomFieldComponent.ts
interface IDashAutoAdminCustomFieldComponent {
    method: 'list' | 'view' | 'edit' | 'create';
    attribute: IDashAutoAdminAttribute;
    resourceConfig: IDashAutoAdminResourceConfig;
    record?: any;
    // Plus any componentProps from schema
}
```

### Example Custom Component

```tsx
// apps/dash/src/components/tab/Tab/TabOrderProductsSelector.tsx
const TabOrderProductsSelector: React.FC<IDashAutoAdminCustomFieldComponent> = ({
    method,
    attribute,
    resourceConfig,
    componentProps
}) => {
    // Access context provided by contextComponent
    const { 
        products, 
        handleProductClick,
        searchFilters 
    } = useTabManager();

    // Different rendering based on method
    if (method === 'list') {
        return <ProductSummary products={products} />;
    }

    if (method === 'create' || method === 'edit') {
        return (
            <ProductSelector
                products={products}
                onSelect={handleProductClick}
                config={componentProps?.config}
            />
        );
    }

    return <ProductDisplay products={products} />;
};
```

---

## Key Interfaces

### IDashAutoAdminResourceConfig

```typescript
interface IDashAutoAdminResourceConfig {
    // Identity
    model: string;                    // API endpoint path
    label: string;                    // Display name
    group?: string;                   // Menu group
    icon?: ReactNode;                 // Menu icon
    
    // Access Control
    roles?: string[];                 // Allowed roles
    
    // Template & Schema
    component: React.ComponentType;   // Usually ResourceTemplate
    schema: IDashAutoAdminAttribute[];
    
    // Context Provider (CRITICAL)
    contextComponent?: React.FC<{
        mode: string;
        resourceConfig: IDashAutoAdminResourceConfig;
        children: ReactNode;
    }>;
    
    // Form Configuration
    formGroupMode?: 'tabs' | 'groups' | 'layout';
    createLayout?: (render: (tabName: string) => ReactNode) => ReactNode;
    editLayout?: (render: (tabName: string) => ReactNode) => ReactNode;
    showLayout?: (render: (tabName: string) => ReactNode) => ReactNode;
    
    // Custom Components
    listComponent?: (config: IDashAutoAdminResourceConfig) => ReactNode;
    showComponent?: (config: IDashAutoAdminResourceConfig) => ReactNode;
    dataGridComponent?: React.ComponentType;
    
    // Drawer Configuration
    drawer?: boolean;
    drawerOptions?: {
        create?: boolean;
        edit?: boolean;
        show?: boolean;
    };
    
    // Behavior
    mutationMode?: 'pessimistic' | 'optimistic' | 'undoable';
    redirectAfterCreate?: string | false;
    redirectAfterUpdate?: string | false;
    refreshAfter?: boolean;
    
    // Field Wrapper (applies to all fields)
    fieldWrapper?: React.FC<IDashAutoAdminCustomFieldComponent>;
}
```

### IDashAutoAdminAttribute

```typescript
interface IDashAutoAdminAttribute {
    // Identity
    attribute: string;                // Field name in data
    label?: string;                   // Display label
    tab?: string;                     // Tab grouping
    
    // Type
    type: StringConstructor | NumberConstructor | BooleanConstructor | 
          DateConstructor | ArrayConstructor | 'custom' | string;
    
    // Visibility per mode
    inList?: boolean;                 // Show in list/datagrid
    inCreate?: boolean;               // Show in create form
    inEdit?: boolean;                 // Show in edit form
    inShow?: boolean;                 // Show in show/view page
    
    // Custom Component
    custom?: boolean;                 // Use custom component
    component?: React.ComponentType<IDashAutoAdminCustomFieldComponent>;
    componentProps?: Record<string, any>;
    
    // Input/Field Props
    inputProps?: Record<string, any>; // Props for form inputs
    fieldProps?: Record<string, any>; // Props for display fields
    
    // Validation
    required?: boolean;
    readOnly?: boolean;
    
    // Sorting
    sortable?: boolean;
    listAttribute?: string;           // Alternative attribute for list sorting
}
```

---

## Debugging & Troubleshooting

### Common Issues

#### 1. "useXxx must be used within a XxxProvider"

**Cause**: Custom component uses a context hook but the context provider isn't wrapping the content.

**Solution**: Ensure `contextComponent` is configured in the resource and handles all modes:

```tsx
const MyContext: IDashAutoAdminResourceConfig["contextComponent"] = ({ mode, children }) => {
    // Must handle ALL modes, including 'show'
    if (mode === "list") {
        return <>{children}</>;  // List may not need provider
    }
    
    return (
        <MyProvider>
            {children}
        </MyProvider>
    );
};
```

#### 2. Custom component not rendering

**Check**:
1. `inCreate`, `inEdit`, `inShow` flags are set correctly
2. `custom: true` is set in attribute
3. `component` is a valid React component

#### 3. Context not available in Show mode

**Historical Issue**: `DashAutoShow.tsx` didn't support `contextComponent`.

**Fix Applied**: Added `ContextComponent` wrapper in `DashAutoShow.tsx` that passes `mode="show"`.

### Debug Logging

Add to your custom components:

```tsx
const MyComponent: React.FC<IDashAutoAdminCustomFieldComponent> = (props) => {
    console.log('🎯 MyComponent render:', {
        method: props.method,
        attribute: props.attribute.attribute,
        hasRecord: !!props.record
    });
    // ...
};
```

---

## Best Practices

### 1. Context Component Design

```tsx
// ✅ Good: Handle all modes explicitly
const MyContext = ({ mode, children }) => {
    switch (mode) {
        case 'list':
            return <ListProvider>{children}</ListProvider>;
        case 'create':
        case 'edit':
        case 'show':
            return <FormProvider>{children}</FormProvider>;
        default:
            return <>{children}</>;
    }
};

// ❌ Bad: Missing modes
const MyContext = ({ mode, children }) => {
    if (mode === 'edit') {
        return <FormProvider>{children}</FormProvider>;
    }
    return <>{children}</>;  // show mode won't have provider!
};
```

### 2. Custom Component Mode Handling

```tsx
// ✅ Good: Handle method variations
const MyField = ({ method }) => {
    switch (method) {
        case 'edit':
        case 'create':
            return <EditableVersion />;
        case 'view':
        case 'show':  // Note: AttributeToField uses 'view'
            return <DisplayVersion />;
        case 'list':
            return <CompactVersion />;
        default:
            return null;
    }
};
```

### 3. Schema Organization

```tsx
// ✅ Good: Group related fields
const schema = [
    // Tab: Basic Info
    { attribute: 'name', tab: 'Basic Info', inCreate: true, inEdit: true },
    { attribute: 'email', tab: 'Basic Info', inCreate: true, inEdit: true },
    
    // Tab: Advanced
    { attribute: 'settings', tab: 'Advanced', inCreate: false, inEdit: true },
    
    // Custom component spanning modes
    { 
        attribute: 'customField', 
        tab: 'Basic Info',
        custom: true,
        component: MyCustomComponent,
        inCreate: true,
        inEdit: true,
        inShow: true,
        inList: false
    }
];
```

---

## File Reference

| File | Purpose |
|------|---------|
| `DashAutoResource.tsx` | Main router for List/Create/Edit/Show |
| `DashAutoList.tsx` | List view renderer |
| `DashAutoCreate.tsx` | Create form wrapper |
| `DashAutoEdit.tsx` | Edit form wrapper |
| `DashAutoShow.tsx` | Show page renderer (with contextComponent) |
| `DashAutoTabbedForm.tsx` | Form renderer (with contextComponent) |
| `DashAutoTabs.tsx` | Tab-based layout for Show |
| `DashAutoGroup.tsx` | Group-based layout |
| `DashAutoLayout.tsx` | Custom layout support |
| `AttributeToInput.tsx` | Schema → Form Input conversion |
| `AttributeToField.tsx` | Schema → Display Field conversion |
| `UserAction.tsx` | Custom component wrapper |
| `interfaces/IDashAutoAdminResourceConfig.ts` | Resource config interface |
| `interfaces/IDashAutoAdminAttribute.ts` | Schema attribute interface |
| `interfaces/IDashAutoAdminCustomFieldComponent.ts` | Custom component props |

---

## Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Initial dash-auto-admin architecture |
| 1.1.0 | Added `contextComponent` support in `DashAutoShow.tsx` |
| 1.1.1 | Fixed `TabsListProvider` to render children |

---

*This documentation is part of the Dash Framework. For questions or contributions, please refer to the project repository.*
