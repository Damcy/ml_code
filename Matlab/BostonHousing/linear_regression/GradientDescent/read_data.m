function [x_train, y_train, x_test, y_test] = read_data()

data = load('housing_train.txt');

x_train = data(:, 1:13);
y_train = data(:, 14);

data = load('housing_test.txt');

x_test = data(:, 1:13);
y_test = data(:, 14);

%scaling 8 11 13
sigma = std(x_train);
mu = mean(x_train);
x_train(:, 2) = (x_train(:, 2) - mu(2)) ./ sigma(2);
x_train(:, 7) = (x_train(:, 7) - mu(7)) ./ sigma(7);
x_train(:, 10) = (x_train(:, 10) - mu(10)) ./ sigma(10);
x_train(:, 11) = (x_train(:, 11) - mu(11)) ./ sigma(11);
x_train(:, 12) = (x_train(:, 12) - mu(12)) ./ sigma(12);
x_train(:, 13) = (x_train(:, 13) - mu(13)) ./ sigma(13);

x_test(:, 2) = (x_test(:, 2) - mu(2)) ./ sigma(2);
x_test(:, 7) = (x_test(:, 7) - mu(7)) ./ sigma(7);
x_test(:, 10) = (x_test(:, 10) - mu(10)) ./ sigma(10);
x_test(:, 11) = (x_test(:, 11) - mu(11)) ./ sigma(11);
x_test(:, 12) = (x_test(:, 12) - mu(12)) ./ sigma(12);
x_test(:, 13) = (x_test(:, 13) - mu(13)) ./ sigma(13);

end