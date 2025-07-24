from symbol_table import SymbolTable

if __name__ == '__main__':
    st = SymbolTable(size=5)

    st.add("a")
    st.add("b")
    st.add("a")
    st.add("c")
    st.add("d")
    st.add("e")
    st.add("f")

    print("Symbol Table Structure:")
    print(st)

    print("\nFind positions of terms:")
    print("Position of 'a':", st.find_position_of_term("a"))
    print("Position of 'b':", st.find_position_of_term("b"))
    print("Position of 'z' (non-existent):", st.find_position_of_term("z"))

    print("\nRetrieve terms by position:")
    pos_a = st.find_position_of_term("a")
    print("Term found at position for 'a':", st.find_by_pos(pos_a))

    pos_nonexistent = st.find_position_of_term("z")
    print("Term found at position for 'z' (non-existent):", st.find_by_pos(pos_nonexistent))

    print("\nCheck if terms exist in the table:")
    print("Contains 'c':", st.contains_term("c"))
    print("Contains 'f':", st.contains_term("f"))
    print("Contains 'z':", st.contains_term("z"))

    st.add("g")
    st.add("h")
    st.add("k")

    print("\nSymbol Table Structure After Adding Colliding Keys:")
    print(st)
