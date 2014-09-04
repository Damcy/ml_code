function [co_y, err] = compare_y(y, y_predict)

[row, column] = size(y);

co_y = [y, y_predict];

err = sum( (y(:,1) - y_predict(:,1)) .^2 ) / row;

end