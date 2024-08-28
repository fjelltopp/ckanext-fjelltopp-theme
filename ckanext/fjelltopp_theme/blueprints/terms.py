import logging
from flask import Blueprint, render_template

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "terms", __name__, url_prefix="/terms"
)


@blueprint.get("/", endpoint="index")
def disclaimer():
    log.debug("Entering disclaimer function")
    return render_template("home/terms.html")
