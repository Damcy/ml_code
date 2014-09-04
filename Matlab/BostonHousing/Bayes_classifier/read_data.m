function [x_train, y_train, x_test, y_test] = read_data()

data = load('housing_train.txt');

x_train = data(:, 1:13);
y_train = data(:, 14);

data = load('housing_test.txt');

x_test = data(:, 1:13);
y_test = data(:, 14);

%高于训练数据的平均值则认为其价格高，反则低
mean_y = mean(y_train);
y_train(:,1) = y_train(:,1) > mean_y;
y_test(:,1) = y_test(:,1) > mean_y;

end