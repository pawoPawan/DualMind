# DualMind Examples

This directory contains example implementations and demonstrations of DualMind features.

## Files

### cloud_rag_example.html
A standalone example demonstrating how to use DualMind's Cloud Mode with RAG (Retrieval Augmented Generation).

**Features Demonstrated:**
- Cloud provider selection (Google, OpenAI, Anthropic, NVIDIA, Azure)
- Model selection from provider
- Embedding provider selection (OpenAI, Google, Cohere, Voyage AI, Hugging Face)
- Dynamic embedding model selection
- Document upload and management
- RAG-enhanced chat with document retrieval

**Usage:**
To use this example, you need to:
1. Start the DualMind server: `./dualmind.sh start`
2. Open the file in a browser: `open examples/cloud_rag_example.html`
3. Or access via server: `http://localhost:8000/static/../examples/cloud_rag_example.html`

**Note:** This is a demonstration file and not part of the core DualMind application. It shows how to integrate Cloud RAG features into your own applications.

## Purpose

These examples are provided to:
- Help developers understand DualMind's capabilities
- Serve as templates for custom implementations
- Demonstrate best practices for using DualMind APIs
- Provide reference implementations

## Not For Production

These files are examples and should not be used directly in production. They are meant for:
- Learning
- Prototyping
- Reference
- Development

For production use, integrate the shown concepts into your main application following the patterns in `/static/local.html` and the cloud mode implementation in `server.py`.

