from __future__ import annotations

from flask import Blueprint, session, redirect, url_for, render_template, flash, g

from src.app.controllers import OrderController
from src.app.routes.user import login_required

admin_area_blueprint = Blueprint("admin_area", __name__, url_prefix="/admin")
admin_product_info_blueprint = Blueprint("admin_product_info", __name__, url_prefix="/admin/products")
admin_orders_info_blueprint = Blueprint("admin_orders_info", __name__, url_prefix="/admin/orders")


@admin_area_blueprint.route("/")
@login_required
def admin_area():
    first_name = session["first_name"]
    if "admin" not in first_name:
        flash("You are not an admin", "warning")
        return redirect(url_for('root.root'))
    return render_template('adminArea.html', firstName=first_name, noOfItems=session["no_of_items"],
                           loggedIn=session["logged_in"])


@admin_product_info_blueprint.route("/")
@login_required
def admin_available_products_statistics():
    return redirect(url_for('root.root'))


@admin_orders_info_blueprint.route("/")
def admin_orders_statistics():
    ses = g.session
    orders = OrderController(ses).get_orders_with_product_info()

    dynamic_data_table = get_dynamic_table(orders)

    return render_template("adminOrderStats.html", cloumnHeaders=dynamic_data_table[0],
                           tableValues=dynamic_data_table[1:],
                           firstName=session["first_name"], noOfItems=session["no_of_items"],
                           loggedIn=session["logged_in"])


def get_dynamic_table(orders: list[list[str | int]]) -> list[list[str | int]]:
    """
    orders besteht aus einer Liste aus Listen. Eine Liste besteht jeweils aus einer order_item_id (int), einer order_id (int) und
    dem product_name (str).

    :param orders: list[list[str | int]] Rohe Daten, aus welchen eine Statistik erstellt wird
    :return: das 2d Array mit der Statistik mit den product_name als Spaltennamen und der order_id als Reihennamen
    """

    # TODO: Code zum fixen des Tests verstehen und Codequalität verbessern
    if not orders:
        return []

    product_names = sorted({order[2] for order in orders})
    order_summary = {}

    for _, order_id, product_name in orders:
        if order_id not in order_summary:
            order_summary[order_id] = {product: 0 for product in product_names}
        order_summary[order_id][product_name] += 1

    headers = ["Order ID"] + product_names
    dynamic_table = [headers]

    for order_id in sorted(order_summary):
        row = [order_id] + [order_summary[order_id][product] for product in product_names]
        dynamic_table.append(row)

    total_row = ["Total"] + [sum(row[i] for row in dynamic_table[1:]) for i in range(1, len(headers))]
    dynamic_table.append(total_row)

    return dynamic_table


def calculate_row_totals(dynamic_table: list[list[str | int]]) -> list[list[str | int]]:
    return dynamic_table


def calculate_column_totals(dynamic_table: list[list[str | int]]) -> list[list[str | int]]:
    pass
