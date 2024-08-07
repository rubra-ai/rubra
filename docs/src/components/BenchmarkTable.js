import React from 'react';
import ModelTable from './ModelTable';

const columns = [
    { Header: 'Model', accessor: 'model' },
    { Header: 'Params (in billions)', accessor: 'params' },
    { Header: 'Function Calling', accessor: 'functionCalling' },
    { Header: 'MMLU (5-shot)', accessor: 'mmlu' },
    { Header: 'GPQA (0-shot)', accessor: 'gpqa' },
    { Header: 'GSM-8K (8-shot, CoT)', accessor: 'gsm8k' },
    { Header: 'MATH (4-shot, CoT)', accessor: 'math' },
    { Header: 'MT-bench', accessor: 'mtBench' },
];

const data = [
    {
        model: 'Gemma-1.1 2B Instruct',
        params: 2.51,
        functionCalling: '-',
        mmlu: '37.84',
        gpqa: '22.99',
        gsm8k: '6.29',
        math: '6.14',
        mtBench: '5.82',
    },
    {
        model: 'Rubra Gemma-1.1 2B Instruct',
        params: 2.84,
        functionCalling: '45.00%',
        mmlu: '38.85',
        gpqa: '24.55',
        gsm8k: '6.14',
        math: '2.38',
        mtBench: '5.75',
    },
    {
        model: 'Llama-3 8B Instruct',
        params: 8.03,
        functionCalling: '-',
        mmlu: '65.69',
        gpqa: '31.47',
        gsm8k: '77.41',
        math: '27.58',
        mtBench: '8.07',
    },
    {
        model: 'Rubra Llama-3 8B Instruct',
        params: 8.9,
        functionCalling: '89.28%',
        mmlu: '64.39',
        gpqa: '31.70',
        gsm8k: '68.99',
        math: '23.76',
        mtBench: '8.03',
    },
    {
        model: 'Llama-3 70B Instruct',
        params: 70.6,
        functionCalling: '-',
        mmlu: '79.90',
        gpqa: '38.17',
        gsm8k: '90.67',
        math: '44.24',
        mtBench: '8.88',
    },
    {
        model: 'Rubra Llama-3 70B Instruct',
        params: 70.6,
        functionCalling: '97.85%',
        mmlu: '75.90',
        gpqa: '33.93',
        gsm8k: '82.26',
        math: '34.24',
        mtBench: '8.36',
    },
    {
        model: 'Mistral 7B Instruct v0.3',
        params: 7.25,
        functionCalling: '22.5%',
        mmlu: '62.10',
        gpqa: '30.58',
        gsm8k: '53.07',
        math: '12.98',
        mtBench: '7.50',
    },
    {
        model: 'Rubra Mistral 7B Instruct v0.3',
        params: 8.12,
        functionCalling: '73.57%',
        mmlu: '59.12',
        gpqa: '29.91',
        gsm8k: '43.29',
        math: '11.14',
        mtBench: '7.69',
    },
    {
        model: 'Mistral 7B Instruct v0.2',
        params: 7.24,
        functionCalling: '-',
        mmlu: '59.27',
        gpqa: '27.68',
        gsm8k: '43.21',
        math: '10.30',
        mtBench: '7.50',
    },
    {
        model: 'Rubra Mistral 7B Instruct v0.2',
        params: 8.11,
        functionCalling: '69.28%',
        mmlu: '58.90',
        gpqa: '29.91',
        gsm8k: '34.12',
        math: '8.36',
        mtBench: '7.36',
    },
    {
        model: 'Phi-3 Mini 128k Instruct',
        params: 3.82,
        functionCalling: '-',
        mmlu: '69.36',
        gpqa: '27.01',
        gsm8k: '83.7',
        math: '32.92',
        mtBench: '8.02',
    },
    {
        model: 'Rubra Phi-3 Mini 128k Instruct',
        params: 4.73,
        functionCalling: '70.00%',
        mmlu: '67.87',
        gpqa: '29.69',
        gsm8k: '79.45',
        math: '30.80',
        mtBench: '8.21',
    },
    {
        model: 'Qwen2-7B-Instruct',
        params: 7.62,
        functionCalling: '-',
        mmlu: '70.78',
        gpqa: '32.14',
        gsm8k: '78.54',
        math: '30.10',
        mtBench: '8.29',
    },
    {
        model: 'Rubra Qwen2-7B-Instruct',
        params: 8.55,
        functionCalling: '85.71%',
        mmlu: '68.88',
        gpqa: '30.36',
        gsm8k: '75.82',
        math: '28.72',
        mtBench: '8.08',
    },
    {
        model: 'Nexusflow/NexusRaven-V2-13B',
        params: 13.0,
        functionCalling: '53.75% ∔',
        mmlu: '43.23',
        gpqa: '28.79',
        gsm8k: '22.67',
        math: '7.12',
        mtBench:'5.36',
    },
    {
        model: 'NousResearch/Hermes-2-Pro-Llama-3-8B',
        params: 8.03,
        functionCalling: '41.25%',
        mmlu: '64.16',
        gpqa: '31.92',
        gsm8k: '73.92',
        math: '21.58',
        mtBench:'7.83',
    },
    {
        model: 'gorilla-llm/gorilla-openfunctions-v2',
        params: 6.91,
        functionCalling: '41.25% ∔',
        mmlu: '49.14',
        gpqa: '23.66',
        gsm8k: '48.29',
        math: '17.54',
        mtBench:'5.13',
    },
    {
        model: 'GPT-4o',
        functionCalling: '98.57%',
        mmlu: '-',
        gpqa: '53.6',
        gsm8k: '-',
        math: '-',
        mtBench:'-',
    },
    {
        model: 'Claude-3.5 Sonnet',
        functionCalling: '98.57%',
        mmlu: '88.7',
        gpqa: '59.4',
        gsm8k: '-',
        math: '-',
        mtBench:'-',
    },
    {
        model: 'Mistral Large (closed-source)',
        functionCalling: '48.60%',
        mmlu: '-',
        gpqa: '-',
        gsm8k: '91.21',
        math: '45.0',
        mtBench:'-',
    },
    {
        model: 'meetkai/functionary-medium-v3.0',
        params: 70.6,
        functionCalling: '46.43%',
        mmlu: '79.85',
        gpqa: '38.39',
        gsm8k: '89.54',
        math: '43.02',
        mtBench:'5.49',
    },
    {
        model: 'meetkai/functionary-small-v2.5',
        params: 8.03,
        functionCalling: '57.14%',
        mmlu: '63.92',
        gpqa: '32.14',
        gsm8k: '66.11',
        math: '20.54',
        mtBench:'7.09',
    },
    {
        model: 'groq/Llama-3-Groq-8B-Tool-Use',
        params: 8.03,
        functionCalling: '45.70%',
        mmlu: '-',
        gpqa: '-',
        gsm8k: '-',
        math: '-',
        mtBench:'-',
    },
    {
        model: 'groq/Llama-3-Groq-70B-Tool-Use',
        params: 70.6,
        functionCalling: '74.29%',
        mmlu: '-',
        gpqa: '-',
        gsm8k: '-',
        math: '-',
        mtBench:'-',
    },
    {
        model: 'Meta/Llama-3.1-8B-Instruct',
        params: 8.03,
        functionCalling: '32.50%',
        mmlu: '-',
        gpqa: '-',
        gsm8k: '-',
        math: '-',
        mtBench:'-',
    },
    {
        model: 'Meta/Llama-3.1-70B-Instruct',
        params: 70.6,
        functionCalling: '63.75%%',
        mmlu: '-',
        gpqa: '-',
        gsm8k: '-',
        math: '-',
        mtBench:'-',
    }
];

function BenchmarkTable() {
    return <ModelTable columns={columns} data={data} />;
}

export default BenchmarkTable;
