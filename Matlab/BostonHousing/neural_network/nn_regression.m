function [w_hide, w_output] = nn_regression(x_train, y_train)

total_iteration = 300000;
err_limit = 0.001;
hide_node = 3;
learn_rate = 0.1;

[row, column] = size(x_train);

w_hide = 0.01 * randn(hide_node, column+1);
w_output = 0.01 * randn(1, hide_node+1);

x_train = [ones(row, 1), x_train];

count = 0;
max = 0;
for index_ite = 1:total_iteration
    temp = mod(index_ite, 433) + 1;
    %计算隐层输出
    o_hide = w_hide * x_train(temp, :)';
    o_hide = sigmf(o_hide, [1, 0]);
    o_hide_add_1 = [1; o_hide];
    
    %计算最终输出
    o_output = w_output * o_hide_add_1;
    o_output = sigmf(o_output, [1, 0]);
    
    %计算误差
    delta_output = o_output * (1 - o_output) * (o_output - y_train(temp));
    delta_hide = delta_output * (o_hide .* (1 - o_hide)) .* w_output(1, 2:hide_node+1)';
    
    err = (o_output - y_train(temp)) * (o_output - y_train(temp));
    if(err < err_limit)
        count = count + 1;
        if count > max
            max = count;
        end
    else
        count = 0;
    end
    if(count > 150) 
        break;
    end
    %更新权值
    w_output = w_output - learn_rate * delta_output * o_hide_add_1';
    w_hide = w_hide - learn_rate * delta_hide * x_train(temp, :);
end


end