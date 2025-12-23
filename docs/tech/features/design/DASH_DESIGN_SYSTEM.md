STYLE SYSTEM:
To add a color: e.g: table-header-color and table-header-bg

In dash-colors.less define the variables.
Dash Colors variables: dash-frontend/packages/dash-styles/src/variables/dash-colors.less

@table-header-color: #999;
@table-header-bg: #CCC;
@table-header-color--light: @table-header-color;
@table-header-bg--light: @table-header-bg;
@table-header-color--dark: #CCC;
@table-header-bg--dark: #999;

Then add the css variables in the Root file.
Dash-Styles Package Root variables ( less as css vars ): 
dash-frontend/packages/dash-styles/src/dash-variables.less

--table-header-color: @table-header-color;
--table-header-color--light: @table-header-color--light;
--table-header-color--dark: @table-header-color--dark;
--table-header-bg: @table-header-bg;
--table-header-bg--light: @table-header-bg--light;
--table-header-bg--dark: @table-header-bg--dark;

If the variables are going to be configurable in backend by the tenant, they must be appended to the default theme_colors settings in 
dash-backend/config/tenants.php 
...
 [
            'id'            => 'theme_colors',
            'group'         => 'theme',
            'tab'           => 'theme',
            'attribute'     => 'settings.' . 'colors',
            ...
            'default_value' => [
                "primary-color--light" => "#41ab5d",
                "btn-danger-color--dark"=> "#d4d4d4",
                ...

                "table-header-color" => "#999",
                "table-header-color--light" => "#999",
                "table-header-color--dark"=> "#CCC",
                "table-header-bg" => "#CCC",
                "table-header-bg--light" => "#CCC",
                "table-header-bg--dark" => "#999"

Then in domain they can be used safely in any style sheet.

.you-class {
    color: var(--table-header-color, @table-header-color);
}

