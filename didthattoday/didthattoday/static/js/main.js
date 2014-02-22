$(document).ready(function() {
    function createHabit(name, description) {
        var editing = ko.observable(false),
            toggleEditMode = function() { editing(!editing()); };
        return {
            name: name,
            description: description,
            editing: editing,
            toggleEditMode: toggleEditMode,
            updateHabit: function () { toggleEditMode(); }
        };
    }

    function habitViewModel() {
        var habits = ko.observableArray(),
            newHabitName = ko.observable(""),
            newHabitDescription = ko.observable("");

        $.getJSON("/habits", function (data) {
            data.habits.forEach(function (habit) {
                habits.push(createHabit(habit.name, habit.description));
            });
        });
        return {
            newHabitName: newHabitName,
            newHabitDescription: newHabitDescription,
            habits : habits,
            addHabit: function () {
                var habit = {name: newHabitName(), description: newHabitDescription()},
                    displayHabit = createHabit(newHabitName(), newHabitDescription());
                $.post('/habit', ko.toJSON(habit), function () { habits.push(displayHabit); });
            }
        };
    }

    ko.applyBindings(habitViewModel());
});
