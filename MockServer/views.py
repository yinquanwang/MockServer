from flask import request, json, render_template, redirect
from flask.views import MethodView
from sqlalchemy import desc
from sqlalchemy.orm.exc import UnmappedInstanceError

from MockServer import models, app, db
from MockServer.common import insert_project, insert_mock_data, update_mock_data
from MockServer.response import VALID, INVALID
from MockServer.validator import domain_server


@app.route('/index/')
def index():
    p = models.Project.query.order_by(desc('id'))
    m = models.Api.query.all()
    return render_template('index.html', p=p, m=m)


class ProjectAPI(MethodView):
    def post(self):
        project_info = request.json
        msg = insert_project(**project_info)
        return json.dumps(msg, ensure_ascii=False)


class MockApi(MethodView):
    def get(self, api_id):
        if api_id:
            pass
        else:
            api_name = request.args.get('api_name')
            m = models.Api.query.filter(models.Api.name.contains(api_name)).all()
            if m:
                p = []
                for moo in m:
                    t_p = models.Project.query.get(moo.project_id)
                    if t_p not in p:
                        p.append(t_p)

                return render_template('index.html', p=p, m=m)
            else:
                return redirect('/index/')

    def post(self):
        mock_info = request.json
        msg = insert_mock_data(**mock_info)
        return json.dumps(msg, ensure_ascii=False)

    def put(self, api_id):
        body = json.loads(request.json)
        try:
            msg = update_mock_data(api_id, **body)
        except UnmappedInstanceError:
            return json.dumps(INVALID, ensure_ascii=False)

        return json.dumps(msg, ensure_ascii=False)

    def delete(self, api_id):
        try:
            m = models.Api.query.get(api_id)
            db.session.delete(m)
            db.session.commit()

        except UnmappedInstanceError:
            return json.dumps(INVALID, ensure_ascii=False)

        return json.dumps(VALID, ensure_ascii=False)


@app.route('/<path:path>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def dispatch_request(path):
    """
    mock view logic
    :param path: request url for mock server
    :return: response msg that use default or custom defined
    """
    m = models.Api.query.filter_by(url=request.path, method=request.method).first_or_404()
    body = json.loads(m.body)
    return domain_server(**body)


@app.errorhandler(404)
def url_not_found(error):
    return json.dumps({
        "status": 404,
        "msg": "the request url not found,please check"
    })
