"""Flask Postgre Compose financial example."""
from os import environ

from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy import create_engine, text
from webargs import fields
from webargs.flaskparser import abort, use_args

app = Flask(__name__)
db = create_engine(environ['DB_STR'])  # 'postgresql://example@localhost:5432/example')


@app.errorhandler(422)
@app.errorhandler(ValidationError)
def handle_error(err):
    """Flask error handler."""
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), 422


@app.errorhandler(400)
def handle_error2(err):
    """Flask error handler."""
    messages = err.data.get("messages", ["Invalid request."])
    return jsonify({"_0": "Internal data mismatch",
                    "errors": messages}), 400


@app.route('/', methods=['POST'])
@use_args({
    'sender': fields.UUID(required=True),
    'receiver': fields.UUID(required=True),
    'amount': fields.Decimal(required=True, validate=lambda x: x > 0)
})
def api_main(args):
    """Put json to DB to make a transaction.

    Example:
        {
            "sender": "40e6815d-b5c6-4896-987c-f30f3678f608",
            "receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
            "amount": 1
        }

    Args:
        args (dict):
            sender (UUID): Person who sends money.
            receiver (UUID): Person who receives money.
            amount (Decimal): transit money amount

    Returns:
        200 and json from DB {"message":"Done successfully"},
        422 error json for a failed validation,
        400 error and one of the below jsons from DB:
                {"error":"Sender is not our client"}
                {"error":"Receiver is not our client"}
                {"error":"Insufficient funds"}
    """
    # process stored procedure
    result = db.execute(
        text(
            'SELECT make_transaction(:sender, :receiver, :amount);'
        ).execution_options(autocommit=True),
        **args
    ).fetchone()[0]

    if 'error' in result:
        abort(400, messages=result['error'])
    else:
        return jsonify(result)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, threaded=True)
