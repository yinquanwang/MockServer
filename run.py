from MockServer import app, views

project_view = views.ProjectAPI.as_view('projects')

app.add_url_rule('/projects/', defaults={'project_id': None}, view_func=project_view, methods=['GET', ])
app.add_url_rule('/projects/', view_func=project_view, methods=['POST', ])
app.add_url_rule('/projects/<int:project_id>/', view_func=project_view, methods=['GET', 'PUT', 'DELETE'])

mock_view = views.MockApi.as_view('mock')

app.add_url_rule('/mocks/', defaults={'api_id': None}, view_func=mock_view, methods=['GET', ])
app.add_url_rule('/mocks/', view_func=mock_view, methods=['POST', ])
app.add_url_rule('/mocks/<int:api_id>/', view_func=mock_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=False)
