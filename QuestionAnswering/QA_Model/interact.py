import time
import argparse
import torch
import msgpack
from QuestionAnswering.QA_Model.drqa.model import DocReaderModel
from QuestionAnswering.QA_Model.drqa.utils import str2bool
from QuestionAnswering.QA_Model.prepro import annotate, to_id, init
from QuestionAnswering.QA_Model.train import BatchGen

def GetEvidence(user_evidence, user_question):
    """
    This script serves as a template to be modified to suit all possible testing environments, including and not limited 
    to files (json, xml, csv, ...), web service, databases and so on.
    To change this script to batch model, simply modify line 70 from "BatchGen([model_in], batch_size=1, ...)" to 
    "BatchGen([model_in_1, model_in_2, ...], batch_size=batch_size, ...)".
    """
    # parser = argparse.ArgumentParser(
    #     description='Interact with document reader model.'
    # )
    # parser.add_argument('--model-file', default='./models/best_model.pt',
    #                     help='path to model file')
    # parser.add_argument("--cuda", type=str2bool, nargs='?',
    #                     const=True, default=torch.cuda.is_available(),
    #                     help='whether to use GPU acceleration.')
    # args = parser.parse_args()

    # print(args)
    model_file="QuestionAnswering/QA_Model/models/best_model.pt"
    cuda=torch.cuda.is_available()
    
    if cuda:
        checkpoint = torch.load(model_file)
    else:
        checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)

    state_dict = checkpoint['state_dict']
    opt = checkpoint['config']
    with open('QuestionAnswering/QA_Model/SQuAD/meta.msgpack', 'rb') as f:
        meta = msgpack.load(f, encoding='utf8')
    embedding = torch.Tensor(meta['embedding'])
    opt['pretrained_words'] = True
    opt['vocab_size'] = embedding.size(0)
    opt['embedding_dim'] = embedding.size(1)
    opt['pos_size'] = len(meta['vocab_tag'])
    opt['ner_size'] = len(meta['vocab_ent'])
    opt['cuda'] = cuda
    BatchGen.pos_size = opt['pos_size']
    BatchGen.ner_size = opt['ner_size']
    model = DocReaderModel(opt, embedding, state_dict)
    w2id = {w: i for i, w in enumerate(meta['vocab'])}
    tag2id = {w: i for i, w in enumerate(meta['vocab_tag'])}
    ent2id = {w: i for i, w in enumerate(meta['vocab_ent'])}
    init()
    id_ = 0
    try:
        while True:
            evidence =user_evidence# input('Evidence: ')
            if evidence.strip():
                break
        while True:
            question =user_question# input('Question: ')
            if question.strip():
                break
    except EOFError:
        print()
    annotated = annotate(('interact-{}'.format(id_), evidence, question), meta['wv_cased'])
    model_in = to_id(annotated, w2id, tag2id, ent2id)
    model_in = next(iter(BatchGen([model_in], batch_size=1, gpu=cuda, evaluation=True)))
    prediction = model.predict(model_in)[0]
    return prediction

