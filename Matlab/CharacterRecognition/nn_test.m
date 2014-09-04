function [y_predict] = nn_test(w_hide, w_output, x_test)

[row, column] = size(x_test);

y_predict = ones(row, 1);

for index_ite = 1:row
o_in = [1, x_test(index_ite, :)];
o_temp = sigmf(w_hide * o_in', [1, 0]);
o_hide = [1, o_temp'];
o_output = sigmf(w_output * o_hide', [1, 0]);

[value, pos] = max(o_output);
y_predict(index_ite) = pos-1;
end


end