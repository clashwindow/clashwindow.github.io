import os
import re

# 配置 _posts 文件夹路径
posts_dir = '_posts'

def clean_description(content):
    # 匹配 Front Matter 中的 description 字段
    # 查找以 description: 开头，直到行尾的内容
    # 使用正则表达式匹配 description: 后面跟随的文本，处理可能存在的引号
    pattern = r'^(description:\s*)(.*)$'
    
    def replacement(match):
        prefix = match.group(1)
        old_desc = match.group(2).strip()
        
        # 去除前后的引号
        clean_desc = old_desc
        if (clean_desc.startswith('"') and clean_desc.endswith('"')) or \
           (clean_desc.startswith("'") and clean_desc.endswith("'")):
            clean_desc = clean_desc[1:-1]
        
        # 提取核心摘要：通常是第一句或前 60 个字符
        # 针对用户文章的特定模式进行精简
        # 模式1: "本文详细介绍[标题]怎么解决还能用吗？，涵盖..." -> 提取到问号或第一个逗号
        core_summary = clean_desc.split('，涵盖')[0].split(', 涵盖')[0].split('。涵盖')[0]
        
        # 模式2: 如果有问号，通常是标题，保留到问号
        if '？' in core_summary:
            core_summary = core_summary.split('？')[0] + '？'
        elif '?' in core_summary:
            core_summary = core_summary.split('?')[0] + '?'
            
        # 模式3: 去除重复的引导语
        core_summary = core_summary.replace('本文详细介绍', '').strip()
        
        # 如果精简后太短（小于10个字），则保留前 80 个字符并截断
        if len(core_summary) < 10:
            core_summary = clean_desc[:80].strip()
            
        # 确保输出是带引号的字符串，防止 YAML 解析出错
        return f'{prefix}"{core_summary}"'

    # 逐行处理以确保只匹配 Front Matter 中的 description
    lines = content.split('\n')
    in_front_matter = False
    new_lines = []
    front_matter_count = 0
    
    for line in lines:
        if line.strip() == '---':
            front_matter_count += 1
            in_front_matter = (front_matter_count == 1)
        
        if in_front_matter and line.startswith('description:'):
            new_lines.append(clean_description_line(line))
        else:
            new_lines.append(line)
            
    return '\n'.join(new_lines)

def clean_description_line(line):
    # 辅助函数，处理单行 description
    prefix = "description: "
    old_desc = line[len(prefix):].strip()
    
    # 去除引号
    clean_desc = old_desc
    if (clean_desc.startswith('"') and clean_desc.endswith('"')) or \
       (clean_desc.startswith("'") and clean_desc.endswith("'")):
        clean_desc = clean_desc[1:-1]
    
    # 精简逻辑
    core_summary = clean_desc.split('，涵盖')[0].split(', 涵盖')[0].split('。涵盖')[0]
    if '？' in core_summary:
        core_summary = core_summary.split('？')[0] + '？'
    elif '?' in core_summary:
        core_summary = core_summary.split('?')[0] + '?'
    
    core_summary = core_summary.replace('本文详细介绍', '').strip()
    
    if len(core_summary) < 10:
        core_summary = clean_desc[:80].strip()
        
    return f'{prefix}"{core_summary}"'

def process_posts():
    if not os.path.exists(posts_dir):
        print(f"Error: Folder {posts_dir} not found.")
        return

    count = 0
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = clean_description(content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
                    print(f"Optimized: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nSuccess! Optimized description for {count} posts.")

if __name__ == "__main__":
    process_posts()
