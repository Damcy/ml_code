function DT(x_train, y_train, name)

tree = classregtree(x_train, y_train, 'names', name);
view(tree);

end