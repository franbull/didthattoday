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
            <h2>Log in</h2>

            % if failed_attempt:
                <p><font color="red">Invalid credentials, try again.</font></p>
            % endif
            <form class="form-inline" role="form"  method="post" action="${ request.path }">
                <div class="form-group">
                    <p>
                        <label for="login">Login</label><br>
                        <input type="text" name="login" value="${ login }">
                    </p>
                    <p>
                        <label for="passwd">Password</label><br>
                        <input type="password" name="passwd">
                    </p>
                    <input type="hidden" name="next" value="${ next }">
                    <input type="submit" name="submit">
                </div>
            </form>
    </body>
</html>
