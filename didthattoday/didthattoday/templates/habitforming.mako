<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link href="${request.static_url('didthattoday:static/bootstrap-3.1.1/css/bootstrap.min.css')}" rel="stylesheet">
    </head>
    <body>
        <script src="${request.static_url('didthattoday:static/knockout.js')}"></script>
        <script src="${request.static_url('didthattoday:static/jquery2.1.0.js')}"></script>
        <script src="${request.static_url('didthattoday:static/bootstrap-3.1.1/js/bootstrap.min.js')}"></script>
        <div class="navbar navbar-inverse navbar-static-top" role="navigation">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#">Habit Forming</a>
                </div>
                <div class="collapse navbar-collapse">
                    <ul class="nav navbar-nav">
                        <li class="active"><a href="#">Behaviors</a></li>
                        <li><a href="#about">Habits</a></li>
                        <li><a href="#contact">Contact</a></li>
                    </ul>
                </div><!--/.nav-collapse -->
            </div>
        </div>

        <div class ='container' role = "main">
            <h2>Behaviors</h2>

            <form class="form-inline" role="form">
                <div class="form-group">
                    <label class="sr-only" for="exampleInputEmail2">Email address</label>
                    <input type="name" id="newHabitName" class="form-control input-sm" placeholder="Habit Name" data-bind="value: newHabitName"/>
                </div>
                <div class="form-group">
                    <label class="sr-only" for="exampleInputPassword2">Password</label>
                    <input type="description" id="newHabit description" class="form-control input-sm" placeholder="Habit description" data-bind="value: newHabitDescription">
                </div>
                <button data-bind="click: addHabit" class="btn btn-sm" type="button">Add</button>
            </form>
            <div class="panel panel-default">
                <!-- Default panel contents -->
                <div class="panel-heading">Behaviors. Things you do.</div>
                <div class="panel-body">
                    <p>A behavior is a thing you do. A habit is a thing you do regularly. What did you do today?</p>
                </div>
                <table class="table table-striped table-hover">
                    <thead>
                    <tr><td>Name</td><td>Description</td></tr>
                    </thead>
                    <tbody  data-bind="foreach: habits">
                    <tr data-bind="visible: editing() == false, click: toggleEditMode">
                        <td data-bind="text: name"/>
                        <td data-bind="text: description"/>
                    </tr>
                    <tr data-bind="visible: editing() == true">
                        <td>
                            <div class="input-group input-group-sm">
                                <span class="input-group-addon">Editing</span>
                                <input type="text" id="existingHabitName" class="form-control" data-bind="value: name"/>
                            </div>
                        </td>
                        <td>
                            <div class="input-group input-group-sm">
                                <input type="text" id="existingHabitDescription" class="form-control" data-bind="value: description"/>
                                <span class="input-group-btn">
                                    <button data-bind="click: updateHabit" class="btn btn-default" type="button">O.K.</button>
                                </span>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <script src="/static/js/main.js"></script>
    </body>
</html>
