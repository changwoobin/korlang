class easy_lang:
  def __init__(self):
      self.data = {}

  @staticmethod
  def checking_type(code):
    if '계속' in code:
      return 'FOR'
    elif '해라' in code:
      return 'END_FOR'
    elif '만약' in code:
      return 'IF'    
    elif '텐데' in code:
      return 'END_IF'
    elif '변수' in code:
      return 'VAR'
    elif '한번' in code:
      return 'PRINT'
    elif '곱하기' in code or '나누기' in code or '더하기' in code or '빼기' in code or '>' in code or '<' in code or '%' in code:
      return 'CAL'
    else:
      return 'ETC'
    
  def condition_calculation(self, code):
    value = code.split(' ')
    exp = ''
    for i in value:
      if i in self.data:
        data = str(self.data[i])
        if data.isdigit():
          exp += data + ' '
        else:
          raise ValueError('변수의 값이 숫자가 아님')
      else:
        exp += i + ' '

    return exp.strip()

  def interpreteLine(self, code, checking_if):
    if code.strip() == '':
      return None
    
    Type = self.checking_type(code)
    if Type == 'VAR' and (checking_if != 0 and checking_if != -1):
      split_code = code.strip().split(' ')
      var_name = split_code[1][:-1]
      c = ''
      for i in split_code:
        if i != '변수' and i != var_name +'는' and i != var_name +'은':
          c += i + ' '
      var_value = c.strip()[:-2]
      var_type = self.checking_type(var_value)
      if var_type == 'CAL':
        cal_value = var_value.split('.')
        exp = ''
        for i in cal_value:
          if i.isdigit():
            exp = exp + i + ' '
          else:
            if i == '곱하기':
              exp = exp+'*'+' '
            elif i == '나누기':
              exp = exp+'/'+' '
            elif i == '더하기':
              exp = exp+'+'+' '
            elif i == '빼기':
              exp = exp+'-'+' '
            elif i in self.data:
              exp = exp + str(self.data[i]) + ' '
            elif i == '%':
              exp = exp + '%' + ' '
      

        self.data[var_name] = eval(exp)
      elif var_type == 'ETC' and (var_value[-1] == "'" and var_value[0] == "'" or var_value[-1] == '"' and var_value[0] == '"'):
        quote = var_value[0]
        self.data[var_name] = var_value.replace(quote, "")
      elif var_value.isdigit():
        self.data[var_name] = int(var_value)
      else:
        raise SyntaxError('문법 에러')
      

      return 1
    
    elif Type == 'PRINT' and (checking_if != 0 and checking_if != -1):
      split_code = code.replace("한번", "").replace("말해봐", "").strip()
      value = split_code[:-1]
      if value in self.data:
        print(self.data[value])
      elif not value.isdigit():
        value_type = self.checking_type(value)
        if value_type == 'CAL':
          cal_value = value.split('.')
          exp = ''
          for i in cal_value:
            if i.isdigit():
              exp = exp + i + ' '
            else:
              if i == '곱하기':
                exp = exp+'*'+' '
              elif i == '나누기':
                exp = exp+'/'+' '
              elif i == '더하기':
                exp = exp+'+'+' '
              elif i == '빼기':
                exp = exp+'-'+' '

          print(eval(exp))
        elif value[-1] == "'" and value[0] == "'" or value[-1] == '"' and value[0] == '"':
          print(value[1:-1])
        else:
          raise SyntaxError('이건 아니다.')
      else:
          print(value)

      return 1
    elif Type == 'IF' and checking_if != -1:
      if checking_if == 0:
        return 6
      
      value = code.strip().split('이면')[0]
      value_condition = value.split('(')[1]
      value_condition = value_condition.replace(')', "")
      condition_checking = self.condition_calculation(value_condition)
      if eval(condition_checking):
        return 5
      else:
        return 0
      
    elif Type == 'END_IF':
      if checking_if == -1:
        return checking_if
      else:
        return 8
    
    elif Type == 'FOR' and (checking_if != 0 and checking_if != -1):
      value = code.split('이라면')[0].replace("계속", "").strip()
      value_condition = value.split('(')[1]
      value_condition = value_condition.replace(')', "")
      condition_checking = self.condition_calculation(value_condition)
      if eval(condition_checking):
        return 2
      else:
        return -1
    
    elif Type == 'END_FOR':
      if checking_if == -1:
        return 4
      else:
        return 3

    elif Type == 'ETC' and '받아라' in code and (checking_if != 0 and checking_if != -1):
      value_text = code.split('라고')[0].replace("이 ", "")
      value_varname = code.split('라고')[1].replace(" 말하고 ", "").replace("에 받아라", "")
      quote = value_text[0]
      value_text = value_text.replace(quote, "")
      value = input(value_text)
      self.data[value_varname] = value
      
    else:
      if checking_if == 0 or checking_if == -1:
        return checking_if
      else:
        raise SyntaxError('구문이 맞지 않습니다.')

  def interprete(self, code):
    spliter = '\n' if '\n' in code else '~'
    code = code.strip().split(spliter)

    index = 0
    for_index = {}
    indexs_for = []
    indexs_if = 0
    checking_if = 1
    while index < len(code):
        line = code[index]
        answer = self.interpreteLine(line, checking_if)
        if answer == None:
          index += 1
          continue
        
        if answer == 2:
          if index - 1 in for_index:
            pass
          else:
            indexs_for.append(index - 1)
            for_index[index - 1] = - 1

        if answer == 3:
          if for_index[indexs_for[-1]] == -1:
            for_index[indexs_for[-1]] = index - 1
          
          index = indexs_for[-1]
        
        checking_if = answer

        if answer == 4:
          if for_index[indexs_for[-1]] != index - 1:
            checking_if = -1
          else:
            del for_index[indexs_for[-1]]
            del indexs_for[-1]

        if answer == 5:
          indexs_if += 1
        
        if answer == 6:
          indexs_if += 1
          checking_if = 0

        if answer == 8:
          indexs_if -= 1
          if indexs_if == 0:
            checking_if = 1

        index += 1