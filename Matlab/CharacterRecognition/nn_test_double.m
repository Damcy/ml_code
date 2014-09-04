function [y_predict] = nn_test_double(w_hide, w_output, x_test)

[row, column] = size(x_test);

y_predict = ones(row, 2);

for index_ite = 1:row
o_in = [1, x_test(index_ite, :)];
o_temp = sigmf(w_hide * o_in', [1, 0]);
o_hide = [1, o_temp'];
o_output = sigmf(w_output * o_hide', [1, 0]);

[value, pos] = max(o_output);
y_predict(index_ite, 1) = pos-1;
o_output(pos) = 0;
[value, pos] = max(o_output);
y_predict(index_ite, 2) = pos-1;
end


end