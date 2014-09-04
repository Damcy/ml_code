function [y_predict] = Bys_predict(x_test, y_high, p_high, p_low, p_4_column, p_9_column)

[row, column] = size(x_test);
y_predict = zeros(row, 1);


%1 / (sqrt(2*pi)*std) * exp(-(x-mean)^2 / (2 * var))
%diff in column 4 and column 9
syms x std_x mean_x var_x;
gaussian = 1 / (sqrt(2*pi)*std_x) * exp(-(x-mean_x)^2 / (2 * var_x));
for index_row = 1:row
    y_1 = y_high;
    y_0 = 1 - y_high;
    for index_col = 1:column
        if index_col == 4
            if(x_test(index_row, 4) == 0)
                y_0 = y_0 * (1 - p_4_column(2));
                y_1 = y_1 * (1 - p_4_column(1));
            else
                y_0 = y_0 * p_4_column(2);
                y_1 = y_1 * p_4_column(1);
            end
        elseif index_col == 9
            y_0 = y_0 * p_9_column(x_test(index_row, 9), 1);
            y_1 = y_1 * p_9_column(x_test(index_row, 9), 1);
        else
            y_0 = y_0 * vpa(subs(gaussian, {x,std_x,mean_x,var_x}, {x_test(index_row, index_col), p_low(index_col, 3), p_low(index_col, 1), p_low(index_col, 2)}));
            y_1 = y_1 * vpa(subs(gaussian, {x,std_x,mean_x,var_x}, {x_test(index_row, index_col), p_high(index_col, 3), p_high(index_col, 1), p_high(index_col, 2)}));
        end
    end
    if y_1 > y_0
        y_predict(index_row) = 1;
    else
        y_predict(index_row) = 0;
    end
end

end