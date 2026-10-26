import matplotlib.pyplot as plt


def plot_monthly_sales(sales):
    """Genera el gráfico de evolución mensual de la facturación."""

    monthly_sales = (
        sales
        .set_index("InvoiceDate")
        .resample("ME")["TotalAmount"]
        .sum()
        .reset_index()
    )

    monthly_sales["Period"] = (
        monthly_sales["InvoiceDate"]
        .dt.strftime("%Y-%m")
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly_sales["Period"],
        monthly_sales["TotalAmount"],
        marker="o"
    )

    plt.title("Evolución mensual de la facturación")
    plt.xlabel("Mes")
    plt.ylabel("Facturación")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def plot_top_products(sales):
    """Genera gráficos de productos por unidades y facturación."""

    excluded_descriptions = [
        "POSTAGE",
        "DOTCOM POSTAGE",
        "Manual"
    ]

    product_data = sales[
        ~sales["Description"].isin(excluded_descriptions)
    ].copy()

    product_sales = (
        product_data
        .groupby("Description")
        .agg(
            UnitsSold=("Quantity", "sum"),
            Revenue=("TotalAmount", "sum")
        )
        .reset_index()
    )

    # Top 10 por unidades vendidas.
    top_units = (
        product_sales
        .sort_values("UnitsSold", ascending=False)
        .head(10)
        .sort_values("UnitsSold")
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top_units["Description"],
        top_units["UnitsSold"]
    )

    plt.title("Top 10 productos por unidades vendidas")
    plt.xlabel("Unidades vendidas")
    plt.ylabel("Producto")

    plt.tight_layout()
    plt.show()

    # Top 10 por facturación.
    top_revenue = (
        product_sales
        .sort_values("Revenue", ascending=False)
        .head(10)
        .sort_values("Revenue")
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top_revenue["Description"],
        top_revenue["Revenue"]
    )

    plt.title("Top 10 productos por facturación")
    plt.xlabel("Facturación")
    plt.ylabel("Producto")

    plt.tight_layout()
    plt.show()


def plot_top_countries(sales):
    """Genera el ranking de países por facturación fuera de Reino Unido."""

    international_sales = sales[
        sales["Country"] != "United Kingdom"
    ].copy()

    country_sales = (
        international_sales
        .groupby("Country")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        country_sales.index,
        country_sales.values
    )

    plt.title("Top 10 países por facturación fuera de Reino Unido")
    plt.xlabel("Facturación")
    plt.ylabel("País")

    plt.tight_layout()
    plt.show()


def plot_top_customers(sales):
    """Genera el ranking de clientes por facturación."""

    customer_sales = sales[
        sales["Customer ID"].notna()
    ].copy()

    customer_summary = (
        customer_sales
        .groupby("Customer ID")["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    customer_ids = (
        customer_summary.index
        .astype(str)
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        customer_ids,
        customer_summary.values
    )

    plt.title("Top 10 clientes por facturación")
    plt.xlabel("Facturación")
    plt.ylabel("Customer ID")

    plt.tight_layout()
    plt.show()


def plot_cancelled_products(df):
    """Genera el ranking de productos por unidades canceladas."""

    cancelled = df[
        df["IsCancelled"]
    ].copy()

    cancelled["CancelledUnits"] = (
        cancelled["Quantity"].abs()
    )

    cancelled_products = (
        cancelled[
            cancelled["Description"] != "Manual"
        ]
        .groupby("Description")["CancelledUnits"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        cancelled_products.index,
        cancelled_products.values
    )

    plt.title("Top 10 productos por unidades canceladas")
    plt.xlabel("Unidades canceladas")
    plt.ylabel("Producto")

    plt.tight_layout()
    plt.show()


def plot_all(df):
    """Genera todas las visualizaciones principales del proyecto."""

    # Las cuatro primeras visualizaciones se basan
    # únicamente en ventas válidas.
    sales = df[
        (~df["IsCancelled"]) &
        (df["Quantity"] > 0) &
        (df["Price"] > 0)
    ].copy()

    plot_monthly_sales(sales)
    plot_top_products(sales)
    plot_top_countries(sales)
    plot_top_customers(sales)

    # El análisis de cancelaciones utiliza el dataset procesado completo.
    plot_cancelled_products(df)