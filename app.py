from flask import Flask,request,jsonify
from prometheus_client import Counter,Histogram,generate_latest
import time


app=Flask(__name__)

# Metrics

REQUEST_COUNT=Counter(
        "request_count",
        "Total number of requests."
        )

ERROR_COUNT=Counter(
        "error_count",
        "Total number of errors."
        )


LATENCY=Histogram(
        "payment_latency_seconds",
        "Payment API latency."
        )


@app.route("/health")
def health():

    REQUEST_COUNT.inc()

    return jsonify(
            {
                "status":"UP"
            }
            )


@app.route("/payment")
def payment():

    REQUEST_COUNT.inc()

    start_time=time.time()

    delay=request.args.get("delay")
    error=request.args.get("error")

    if delay:

        time.sleep(int(delay))


    if error=="true":

        ERROR_COUNT.inc()

        return jsonify(
                {
                    "status":"FAILED"
                }
                ),500


    LATENCY.observe(
            time.time()-start_time
            )

    return jsonify(
            {
                "status":"SUCCESS"
            }
            )


@app.route("/metrics")
def metrics():

    return generate_latest(),200


if __name__=="__main__":

    app.run(
            host="0.0.0.0",
            port=5000
            )
