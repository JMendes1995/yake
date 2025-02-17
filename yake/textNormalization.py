import re


def format_one_gram_text(text, relevant_words_array):
    text_tokens = text.replace('\n',' ').split(' ')
    try:
        for tk in range(len(text_tokens)):
            kw = re.sub('[!",:.;?()]$|^[!",:.;?()]|\W["!,:.;?()]', '',  text_tokens[tk]).lower()
            if kw in relevant_words_array:
                text_tokens[tk] = text_tokens[tk].lower().replace(kw, '<kw>' + kw + '</kw>')
    except:
        pass
    new_text = ' '.join(text_tokens)
    return new_text


def format_n_gram_text(text, relevant_words_array, n_gram):
    text_tokens = text.replace('\n',' ').split(' ')
    y = 0
    final_splited_text = []
    while y < len(text_tokens):

        splited_n_gram_kw_list = []
        n_gram_kw_list = []
        n_gram_word_list, splited_n_gram_kw_list = find_more_relevant(y, text_tokens, n_gram, relevant_words_array, n_gram_kw_list, splited_n_gram_kw_list)
        if n_gram_word_list:

            if len(n_gram_word_list[0].split(' ')) == 1:
                y, new_expression = replace_token(text_tokens, y, n_gram_word_list)
                final_splited_text.append(new_expression)
            else:
                kw_list = []
                splited_n_gram_kw_list = []
                splited_one = n_gram_word_list[0].split()

                for len_kw in range(0, len(splited_one)):
                    kw_list, splited_n_gram_kw_list = find_more_relevant(y+len_kw, text_tokens, n_gram, relevant_words_array, kw_list, splited_n_gram_kw_list)
                min_score_word = min(kw_list, key=lambda x: relevant_words_array.index(x))

                if kw_list.index(min_score_word) == 0:
                    term_list = [min_score_word]
                    y, new_expression = replace_token(text_tokens, y, term_list)
                    final_splited_text.append(new_expression)

                elif kw_list.index(min_score_word) >= 1:
                    index_of_more_relevant = splited_n_gram_kw_list[0].index(min_score_word.split()[0])
                    temporal_kw = ' '.join(splited_n_gram_kw_list[0][:index_of_more_relevant])
                    if temporal_kw.lower() in relevant_words_array:

                        if relevant_words_array.index(temporal_kw.lower()) > relevant_words_array.index(final_splited_text[-1].lower() +' '+temporal_kw.lower()) and not re.findall('<kw>', final_splited_text[-1].lower()):
                            term_list = [final_splited_text[-1].lower() +' '+temporal_kw.lower()]
                            del final_splited_text[-1]
                            y -= 1
                            y, new_expression = replace_token(text_tokens, y, term_list)
                            final_splited_text.append(new_expression)
                        else:
                            term_list = [temporal_kw.lower()]
                            y, new_expression = replace_token(text_tokens, y, term_list)
                            final_splited_text.append(new_expression)
                    else:
                        for tmp_kw in splited_n_gram_kw_list[0][:index_of_more_relevant]:
                            if tmp_kw.lower() in relevant_words_array:
                                    term_list = [tmp_kw.lower()]
                                    y, new_expression = replace_token(text_tokens, y, term_list)
                                    final_splited_text.append(new_expression)
                            else:
                                final_splited_text.append(text_tokens[y])
                                y += 1

        else:
            final_splited_text.append(text_tokens[y])
            y += 1
    new_text = ' '.join(final_splited_text)

    return new_text


def find_more_relevant(y, text_tokens, n_gram, relevant_words_array, kw_list, splited_n_gram_word_list):
    temporary_list = []
    temporary_list_two = []
    for i in range(n_gram):

        temporary_list.append(text_tokens[y:y + i + 1])
        k = re.sub('''[!",:.;?()]$|^[!",':.;?()]|\W["!,:.;?()]''', '',  ' '.join(temporary_list[i])).lower()

        if k.lower() in relevant_words_array:
            temporary_list_two.append(k)

    n_gram_word_list = sorted(temporary_list_two, key=lambda x: relevant_words_array.index(x))

    try:
        kw_list.append(n_gram_word_list[0])
        splited_n_gram_word_list.append(n_gram_word_list[0].split())
    except:
        pass

    return kw_list, splited_n_gram_word_list


def replace_token(text_tokens, y, n_gram_word_list):
    txt = ' '.join(text_tokens[y:y + len(n_gram_word_list[0].split(' '))])

    new_expression = txt.replace(re.sub('[!",:.;?()]$|^[!",:.;?()]|\W["!,:.;?()]', '',  txt), '<kw>' + n_gram_word_list[0] + '</kw>')
    y += len(n_gram_word_list[0].split(' '))
    return y, new_expression