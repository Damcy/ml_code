function [y_high, p_high, p_low, p_4_column, p_9_column] = Bys_learn(x, y)

[row, column] = size(x);

high = sum(y);
low = row - high;
y_high = high/row;

p_high = zeros(column, 3);
p_low = zeros(column, 3);
for index_col = 1:column
    high_temp = 1;
    low_temp = 1;
    vector_high = zeros(high, 1);
    vector_low = zeros(low, 1);
    %�����ÿһ�е�����
    for index_row = 1:row
        if y(index_row) == 1
            vector_high(high_temp, 1) = x(index_row, index_col);
            high_temp = high_temp + 1; 
        else
            vector_low(low_temp, 1) = x(index_row, index_col);
            low_temp = low_temp + 1;
        end
    end
    %���Ӧ��ľ�ֵ����
    mean_high = mean(vector_high);
    std_high = std(vector_high);
    var_high = var(vector_high);
    mean_low = mean(vector_low);
    std_low = std(vector_low);
    var_low = var(vector_low);
    %save
    p_high(index_col, :) = [mean_high, var_high, std_high];
    p_low(index_col, :) = [mean_low, var_low, std_low];
end



%��������е�0 1���� 
%p_4_column��һ������Ϊ1�ĸ��� �ڶ���Ϊ1��1�еĸ��� ������Ϊ1��0�еĸ���
p_1 = 0;
p_1_1 = 0;
p_1_0 = 0;
for index_row = 1:row
    if x(index_row, 4) == 1
        p_1 = p_1 + 1;
        if y(index_row) == 1
            p_1_1 = p_1_1 + 1;
        else
            p_1_0 = p_1_0 + 1;
        end
    end
end
p_4_column = [p_1_1/high, p_1_0/low];


%����ھ��еĸ��� 1-24
p_1 = zeros(24, 1);
p_1_1 = zeros(24, 1);
p_1_0 = zeros(24, 1);
for index_row = 1:row
    p_1(x(index_row, 9), 1) = p_1(x(index_row, 9), 1) + 1;
    if y(index_row) == 1
        p_1_1(x(index_row, 9), 1) = p_1_1(x(index_row, 9), 1) + 1;
    else
        p_1_0(x(index_row, 9), 1) = p_1_0(x(index_row, 9), 1) + 1;
    end
end
p_1_1 = p_1_1 ./ high;
p_1_0 = p_1_0 ./low;
p_9_column = [p_1_1, p_1_0];

end