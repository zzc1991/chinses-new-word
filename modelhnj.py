import math
class Node(object):

    def __init__(self, char):
        self.char = char

        self.word_finish = False

        self.count = 0

        self.child = {}

        self.isback = False


class TrieNode(object):

    def __init__(self, node, data=None, PMI_limit=20):

        self.root = Node(node)
        self.PMI_limit = PMI_limit
        if not data:
            return
        node = self.root
        for key, values in data.items():
            if key[0] in node.child:
                node_f = node.child[key[0]]
                new_node = Node(key)
                new_node.count = int(values)
                new_node.word_finish = True
                node_f.append(new_node)
                node.child[key[0]] = node_f
            else:
                new_node = Node(key)
                new_node.count = int(values)
                new_node.word_finish = True
                node.child[key[0]] = [new_node]

    def get_nodef_value(self, char):
        node = self.root
        value_list = node.child[char]
        for value in value_list:
            print(value.char, value.count)

    def add(self, word):
        node = self.root
        for count, char in enumerate(word):
            found_in_child = False
            if char[0] in node.child:
                for child in node.child[char[0]]:
                    if char == child.char:
                        node = child
                        found_in_child = True
                        break

            if not found_in_child:
                if char[0] in node.child:
                    node_f = node.child[char[0]]
                    new_node = Node(char)
                    node_f.append(new_node)
                    node = new_node
                else:
                    new_node = Node(char)
                    node.child[char[0]] = [new_node]
                    node = new_node

            if count == len(word) - 1:
                node.count += 1
                node.word_finish = True

        length = len(word)
        node = self.root
        if length == 3:
            word = list(word)
            word[0], word[1], word[2] = word[1], word[2], word[0]

            for count, char in enumerate(word):
                found_in_child = False
                if count != length - 1:
                    if char[0] in node.child:
                        for child in node.child[char[0]]:
                            if char == child.char:
                                node = child
                                found_in_child = True
                                break
                else:
                    if char[0] in node.child:
                        for child in node.child[char[0]]:
                            if char == child.char and child.isback:
                                node = child
                                found_in_child = True
                                break

                if not found_in_child:
                    new_node = Node(char)
                    if char[0] in node.child:
                        node.child[char[0]].append(new_node)
                    else:
                        node.child[char[0]] = [new_node]
                    node = new_node

                if count == len(word) - 1:
                    node.count += 1
                    node.isback = True
                    node.word_finish = True

    def search_one(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        total = 0
        for node_f in node.child:
            for child in node.child[node_f]:
                if child.word_finish is True:
                    total += child.count

        for node_f in node.child:
            for child in node.child[node_f]:
                if child.word_finish is True:
                    result[child.char] = child.count / total

        return result, total

    def search_bi(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        total = 0
        one_dict, total_one = self.search_one()

        for child_f in node.child:
            for child in node.child[child_f]:
                for ch_f in child.child:
                    for ch in child.child[ch_f]:
                        if ch.word_finish is True:
                            total += ch.count

        for child_f in node.child:
            for child in node.child[child_f]:
                for ch_f in child.child:
                    for ch in child.child[ch_f]:
                        if ch.word_finish is True:
                            PMI = math.log(max(ch.count, 1), 2) - math.log(total, 2) - math.log(one_dict[child.char],
                                                                                                2) - math.log(
                                one_dict[ch.char],
                                2)
                            if PMI > self.PMI_limit:
                                result[child.char + '_' + ch.char] = (PMI, ch.count / total)

        return result

    def search_left(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        for child_f in node.child:
            for child in node.child[child_f]:
                for ch_f in child.child:
                    for cha in child.child[ch_f]:
                        total = 0
                        p = 0.0
                        for cha_f in cha.child:
                            for ch in cha.child[cha_f]:
                                if ch.word_finish is True and ch.isback:
                                    total += ch.count
                            for ch in cha.child[cha_f]:
                                if ch.word_finish is True and ch.isback:
                                    p += (ch.count / total) * math.log(ch.count / total, 2)
                        # 计算的是信息熵
                        result[child.char + cha.char] = -p

        return result

    def search_right(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        for child_f in node.child:
            for child in node.child[child_f]:
                for ch_f in child.child:
                    for cha in child.child[ch_f]:
                        total = 0
                        p = 0.0
                        for cha_f in cha.child:
                            for ch in cha.child[cha_f]:
                                if ch.word_finish is True and not ch.isback:
                                    total += ch.count
                            for ch in cha.child[cha_f]:
                                if ch.word_finish is True and not ch.isback:
                                    p += (ch.count / total) * math.log(ch.count / total, 2)
                        result[child.char + cha.char] = -p
        return result

    def find_word(self, N):

        bi = self.search_bi()
        left = self.search_left()
        right = self.search_right()
        result = {}
        for key, values in bi.items():
            print(key)
            d = "".join(key.split('_'))
            result[key] = (values[0] + min(left[d], right[d])) * values[1]
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print("result: ", result)
        dict_list = [result[0][0]]
        add_word = {}
        new_word = "".join(dict_list[0].split('_'))
        add_word[new_word] = result[0][1]
        for d in result[1: N]:
            flag = True
            for tmp in dict_list:
                pre = tmp.split('_')[0]
                if d[0].split('_')[-1] == pre or "".join(tmp.split('_')) in "".join(d[0].split('_')):
                    flag = False
                    break
            if flag:
                new_word = "".join(d[0].split('_'))
                add_word[new_word] = d[1]
                dict_list.append(d[0])

        return result, add_word
