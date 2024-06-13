import json
import csv
import argparse

def generate_scores_by_format_and_tag(file_path):
    # 初始化分数存储和计数
    scores = {
        'Knowledge': {'total_score': 0, 'total_count': 0},
        'Reasoning': {'total_score': 0, 'total_count': 0},
        'Overall': {'total_score': 0, 'total_count': 0}
    }
    formats = ['Multiple-choice', 'Assertion', 'Fill-in-the-blank', 'Open-ended']

    # 为每个Tag和Format初始化分数和计数
    for tag in ['Knowledge', 'Reasoning', 'Overall']:
        for format_type in formats:
            scores[tag][format_type] = {'score': 0, 'count': 0}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                if 'score' not in data:
                    continue
                
                score = data['score']
                format_type = data['Format']
                tag = data['Tag']
                
                # 更新Tag和Format的分数和计数
                if format_type in formats and tag in ['Knowledge', 'Reasoning']:
                    scores[tag][format_type]['score'] += score
                    scores[tag][format_type]['count'] += 1
                    scores[tag]['total_score'] += score
                    scores[tag]['total_count'] += 1
                    
                    # 更新总体分数和计数
                    scores['Overall'][format_type]['score'] += score
                    scores['Overall'][format_type]['count'] += 1
                    scores['Overall']['total_score'] += score
                    scores['Overall']['total_count'] += 1

        # 输出到CSV文件
        with open('scores_by_format_and_tag.csv', 'w', newline='') as csvfile:
            fieldnames = ['Tag'] + formats + ['All']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for tag in ['Knowledge', 'Reasoning', 'Overall']:
                row = {'Tag': tag}
                for format_type in formats:
                    if scores[tag][format_type]['count'] > 0:
                        avg_score = scores[tag][format_type]['score'] / scores[tag][format_type]['count']
                    else:
                        avg_score = 0
                    row[format_type] = f"{avg_score:.2f}"
                
                # 计算总平均分
                if scores[tag]['total_count'] > 0:
                    overall_avg = scores[tag]['total_score'] / scores[tag]['total_count']
                else:
                    overall_avg = 0
                row['All'] = f"{overall_avg:.2f}"
                
                writer.writerow(row)

    except Exception as e:
        print(f'An error occurred: {e}')

def generate_scores_by_domain_and_tag(file_path):
    # 定义Domain和Tags
    domains = ['Computer Organization', 'Data Structure and Algorithm', 'Operating System', 'Computer Network', 'All']
    tags = ['Knowledge', 'Reasoning', 'Overall']

    # 初始化分数存储和计数
    scores = {tag: {domain: {'total_score': 0, 'total_count': 0} for domain in domains} for tag in tags}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                if 'score' not in data or 'Domain' not in data:
                    continue
                
                score = data['score']
                domain = data['Domain']
                tag = data['Tag']
                
                # 检查Domain是否在我们的列表中，更新对应Tag和Domain的分数和计数
                if domain in domains[:-1] and tag in ['Knowledge', 'Reasoning']:
                    scores[tag][domain]['total_score'] += score
                    scores[tag][domain]['total_count'] += 1
                    scores['Overall'][domain]['total_score'] += score
                    scores['Overall'][domain]['total_count'] += 1
                    
                    # 更新“All”分类
                    scores[tag]['All']['total_score'] += score
                    scores[tag]['All']['total_count'] += 1
                    scores['Overall']['All']['total_score'] += score
                    scores['Overall']['All']['total_count'] += 1

        # 输出到CSV文件
        with open('scores_by_domain_and_tag.csv', 'w', newline='') as csvfile:
            fieldnames = ['Tag'] + domains
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for tag in tags:
                row = {'Tag': tag}
                for domain in domains:
                    if scores[tag][domain]['total_count'] > 0:
                        avg_score = scores[tag][domain]['total_score'] / scores[tag][domain]['total_count']
                    else:
                        avg_score = 0
                    row[domain] = f"{avg_score:.2f}"
                
                writer.writerow(row)

    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file_path', type=str, help='The path to the input JSON file')
    
    args = parser.parse_args()
    generate_scores_by_format_and_tag(args.file_path)
    generate_scores_by_domain_and_tag(args.file_path)

if __name__ == "__main__":
    main()
