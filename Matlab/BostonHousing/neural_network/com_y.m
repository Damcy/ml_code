function [co_y, mean_err] = com_y(y_predict, y_test)

co_y = [y_predict, y_test];

mean_err = sqrt(sum( (y_predict - y_test) .^ 2 ) / 74);

end