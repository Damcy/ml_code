function [x, y, x_train, y_train, x_test, y_test, name] = read_data()

x = load('result.txt');
y = load('mark.txt');

x_train = x(1:230, :);
y_train = y(1:230, :);

x_test = x(231:294, :);
y_test = y(231:294, :);

name = {'length'; 'doc'; 'vowel'; 'first_vowel'; 'second_vowel'; 'link'; 'non_vowel'; 'odd_even'; 'space'};
end