#
#

# 检查
def check_banned_word(text, banned_words):
    # 按照敏感词的长度降序排列，以确保较长的词先被替换
    banned_words = sorted(banned_words, key=len, reverse=True)

    for word in banned_words:
        if word in text:
            text = text.replace(word, f'<span style="background-color: red;color: #f5f5f5">{word}</span>')

    return text


def check_banned_word_list(text, banned_words):
    reslist = []
    for word in banned_words:
        if word.risk_name in text:
            reslist.append(
                {'id': word.id, 'risk_name': word.risk_name, 'risk_level': word.risk_level, 'reason': word.reason})

    return reslist


def check_banned_word_list_text(text, riskList):
    banned_word = [it.risk_name for it in riskList]
    data = {'resultText': check_banned_word(text, banned_word), 'riskList': check_banned_word_list(text, riskList)}
    return data
